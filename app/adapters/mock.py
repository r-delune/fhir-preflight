"""Deterministic stand-in; never contacts a model service."""


class MockModelAdapter:
    model_id = "mock-step-0"

    def describe(self) -> str:
        return "Mock adapter: no AI model is connected."
