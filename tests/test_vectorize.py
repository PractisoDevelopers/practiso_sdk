import asyncio
import inspect
import os
from unittest import TestCase

import practiso_sdk.archive as archive
import practiso_sdk.google.ai


def asyncio_run(async_func):
    def wrapper(*args, **kwargs):
        return asyncio.run(async_func(*args, **kwargs))

    wrapper.__signature__ = inspect.signature(async_func)  # without this, fixtures are not injected

    return wrapper


class TestGeminiAgent(TestCase):
    sample_quiz = archive.Quiz(
        name=None,
        frames=[
            archive.Text('Which layer of the OSI model is responsible for error detection and correction?'),
            archive.Options([
                archive.OptionItem(archive.Text('Physical')),
                archive.OptionItem(archive.Text('Data Link')),
                archive.OptionItem(archive.Text('Network')),
                archive.OptionItem(archive.Text('Transport'))
            ])
        ],
        dimensions=[]
    )

    @asyncio_run
    async def test_get_dimensions(self):
        agent = practiso_sdk.google.ai.GeminiAgent(api_key=os.environ['GEMINI_API_KEY'])
        dimensions = await agent.get_dimensions(self.sample_quiz)
        print(dimensions)
        self.assertGreaterEqual(len(dimensions), 2)
