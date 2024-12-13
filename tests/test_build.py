import os
import unittest
from unittest import TestCase

import practiso_sdk.archive as archive
import practiso_sdk.google.ai
from practiso_sdk import build
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
