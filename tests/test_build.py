import asyncio
import os
import unittest
from unittest import TestCase

import practiso_sdk.google.ai
from practiso_sdk import archive
from practiso_sdk import build
from practiso_sdk.archive import Quiz, Dimension
from tests import asyncio_run

sample_quiz = archive.Quiz(
    name=None,
    frames=[
        archive.Text('Which layer of the OSI model is responsible for error detection and correction?'),
        archive.Options([
            archive.OptionItem(archive.Text('Physical')),
            archive.OptionItem(archive.Text('Data Link')),
            archive.OptionItem(archive.Text('Network')),
            archive.OptionItem(archive.Text('Transport'), is_key=True)
        ])
    ],
    dimensions=[]
)


class TestGeminiAgent(TestCase):
    @asyncio_run
    async def test_get_dimensions(self):
        agent = practiso_sdk.google.ai.GeminiAgent(api_key=os.environ['GEMINI_API_KEY'])
        dimensions = await agent.get_dimensions(sample_quiz)
        print(dimensions)
        self.assertGreaterEqual(len(dimensions), 2)


class PrintAgent(build.VectorizeAgent):
    counter = 0
    __msg: str

    def __init__(self, msg: str):
        self.__msg = msg

    async def get_dimensions(self, quiz: Quiz) -> set[Dimension]:
        print(f'Request {self.counter}, {self.__msg}')
        self.counter += 1
        return set()


class TestRateLimit(TestCase):
    @staticmethod
    async def run_continuous(size: int, agent: build.VectorizeAgent):
        await asyncio.gather(*(agent.get_dimensions(sample_quiz) for _ in range(size)))

    @asyncio_run
    async def test_r3b1_c6(self):
        r3b1 = build.RateLimitedVectorizeAgent(PrintAgent('RPM3, batch1'), rpm=3, batch_size=1)
        await self.run_continuous(6, r3b1)

    @asyncio_run
    async def test_r160b20_c42(self):
        r20b20 = build.RateLimitedVectorizeAgent(PrintAgent('RPM160, batch20'), rpm=160, batch_size=20)
        await self.run_continuous(42, r20b20)


class TestBuilder(TestCase):
    @asyncio_run
    async def test_builder(self):
        builder = build.Builder()
        builder.begin_quiz(creation_time=sample_quiz.creation_time) \
            .add_text('Which layer of the OSI model is responsible for error detection and correction?') \
            .begin_options() \
            .begin_option(is_key=True, priority=0) \
            .add_text('Transport') \
            .end_option() \
            .begin_option(priority=0) \
            .add_text('Network') \
            .end_option() \
            .begin_option() \
            .add_text('Physical') \
            .end_option() \
            .begin_option() \
            .add_text('Data Link') \
            .end_option() \
            .end_options() \
            .end_quiz()

        built = await builder.build(vectorizer=build.DefaultVectorizeAgent(sample_quiz.dimensions))
        self.assertEqual(built.content[0], sample_quiz)


if __name__ == '__main__':
    unittest.main()
