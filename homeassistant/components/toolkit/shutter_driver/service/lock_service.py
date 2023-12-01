import threading
import time


class LockService:
    def __init__(self) -> None:
        self.main_synchronization_lock = threading.RLock()
        self.group_synchronization_locks: dict = {}
        self.lock_group_values: dict = {}

    def ensure_group_lock(self, lock_group_key: str) -> int:
        with self.main_synchronization_lock:
            if lock_group_key not in self.lock_group_values.keys():
                self.lock_group_values[lock_group_key] = 0
                self.group_synchronization_locks[lock_group_key] = threading.RLock()
        return time.time_ns()

    def is_lock_acquired(self, lock_group_key: str, lock_value: int) -> bool:
        with self.group_synchronization_locks[lock_group_key]:
            return self.lock_group_values[lock_group_key] == lock_value

    def acquire_lock(self, lock_group_key: str, lock_value: int) -> bool:
        with self.group_synchronization_locks[lock_group_key]:
            lock_acquired = False
            if self.lock_group_values[lock_group_key] == 0:
                self.lock_group_values[lock_group_key] = lock_value
                lock_acquired = True
            return lock_acquired

    def steal_lock(self, lock_group_key: str, lock_value: int):
        with self.group_synchronization_locks[lock_group_key]:
            self.lock_group_values[lock_group_key] = lock_value

    def force_release_lock(self, lock_group_key: str):
        with self.group_synchronization_locks[lock_group_key]:
            self.lock_group_values[lock_group_key] = 0

    def release_lock(self, lock_group_key: str, lock_value: int):
        with self.group_synchronization_locks[lock_group_key]:
            if self.lock_group_values[lock_group_key] == lock_value:
                self.lock_group_values[lock_group_key] = 0
