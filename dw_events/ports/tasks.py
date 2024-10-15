from abc import ABCMeta, abstractmethod


__all__ = [
    'TaskProgressCallback',
    'TaskETACallback',
    'TaskProgressListenerInterface',
    'TaskETAListenerInterface',
]


class TaskProgressCallback(metaclass=ABCMeta):
    @abstractmethod
    def set_progress(self, percentage: float) -> None:
        pass


class TaskETACallback(metaclass=ABCMeta):
    @abstractmethod
    def set_eta(self, seconds: float) -> None:
        pass


class TaskProgressListenerInterface(metaclass=ABCMeta):
    @abstractmethod
    def add_progress_callback(self, callback: TaskProgressCallback):
        pass

    @abstractmethod
    def remove_progress_callback(self, callback: TaskProgressCallback):
        pass

    @abstractmethod
    def set_progress(self, percentage: float):
        pass


class TaskETAListenerInterface(metaclass=ABCMeta):
    @abstractmethod
    def add_eta_callback(self, callback: TaskETACallback):
        pass

    @abstractmethod
    def remove_eta_callback(self, callback: TaskETACallback):
        pass

    @abstractmethod
    def set_eta(self, eta: float):
        pass


class BackgroundTask(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass
