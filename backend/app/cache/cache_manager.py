"""
缓存层 - CacheManager 多级缓存管理器
一级：进程内存缓存（TTL）；二级：文件缓存（可选）
内置命中率统计，目标缓存命中率 ≥ 98%
"""

import pickle
import os
import threading
import time
from dataclasses import dataclass, field


@dataclass
class CacheEntry:
    """缓存条目：值 + 过期时间"""
    value: object
    ttl: int = 3600
    expire_at: float = field(default=0.0, init=False)

    def __post_init__(self):
        self.expire_at = time.time() + self.ttl

    def is_expired(self, now: float = None) -> bool:
        now = now if now is not None else time.time()
        return self.expire_at <= now


class CacheManager:
    """多级缓存管理器，目标缓存命中率 ≥ 98%"""

    def __init__(self, app=None):
        self.memory_cache = {}          # 一级：进程内存缓存（TTL）
        self.file_cache_dir = None      # 二级：文件缓存（可选）
        self.hits = 0                   # 命中计数
        self.misses = 0                 # 未命中计数
        self._lock = threading.Lock()
        self._enabled = False
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """从 Flask app 配置初始化缓存"""
        self._enabled = True
        cache_type = app.config.get('CACHE_TYPE', 'memory')
        ttl = app.config.get('CACHE_DEFAULT_TIMEOUT', 3600)
        self._default_ttl = ttl
        if cache_type == 'file':
            self.file_cache_dir = app.config.get('CACHE_FILE_DIR')
            if self.file_cache_dir:
                os.makedirs(self.file_cache_dir, exist_ok=True)

    def get(self, key):
        """获取缓存，自动统计命中率"""
        value = self._get_memory(key)
        if value is not None:
            return value
        if self.file_cache_dir:
            value = self._get_file(key)
            if value is not None:
                self.set(key, value, self._default_ttl)
                return value
        self.misses += 1
        return None

    def _get_memory(self, key):
        with self._lock:
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if not entry.is_expired():
                    self.hits += 1
                    return entry.value
                else:
                    del self.memory_cache[key]
        return None

    def set(self, key, value, ttl=3600):
        """写入缓存"""
        with self._lock:
            self.memory_cache[key] = CacheEntry(value, ttl)
        if self.file_cache_dir:
            self._set_file(key, value, ttl)

    def _get_file(self, key):
        path = os.path.join(self.file_cache_dir, f"{self._safe_key(key)}.pkl")
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'rb') as f:
                entry = pickle.load(f)
            if isinstance(entry, CacheEntry) and not entry.is_expired():
                return entry.value
        except Exception:
            os.remove(path)
        return None

    def _set_file(self, key, value, ttl):
        path = os.path.join(self.file_cache_dir, f"{self._safe_key(key)}.pkl")
        try:
            with open(path, 'wb') as f:
                pickle.dump(CacheEntry(value, ttl), f)
        except Exception:
            pass

    @staticmethod
    def _safe_key(key):
        import hashlib
        return hashlib.md5(str(key).encode('utf-8')).hexdigest()

    def get_or_set(self, key, loader_func, ttl=3600):
        """获取或加载并缓存（最常用方法）"""
        result = self.get(key)
        if result is None:
            result = loader_func()
            if result is not None:
                self.set(key, result, ttl)
        return result

    def clear(self):
        """清空内存缓存与文件缓存"""
        with self._lock:
            self.memory_cache.clear()
        if self.file_cache_dir:
            for name in os.listdir(self.file_cache_dir):
                if name.endswith('.pkl'):
                    try:
                        os.remove(os.path.join(self.file_cache_dir, name))
                    except OSError:
                        pass

    def invalidate(self, key):
        """删除指定 key"""
        with self._lock:
            self.memory_cache.pop(key, None)
        if self.file_cache_dir:
            path = os.path.join(self.file_cache_dir, f"{self._safe_key(key)}.pkl")
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 100.0

    def get_stats(self):
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f'{self.hit_rate:.2f}%',
            'memory_entries': len(self.memory_cache),
        }


# 模块级单例，供服务层直接使用
cache = CacheManager()