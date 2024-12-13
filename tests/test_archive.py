import unittest
from io import BytesIO
from xml.etree.ElementTree import ElementTree

import practiso_sdk.archive as archive


class ArchiveTestCase(unittest.TestCase):
    sample_quiz_set = archive.QuizContainer(content=[archive.Quiz(
        name='Test quiz 1',
        frames=[
            archive.Text('Hi I am text frame by test quiz 1'),
            archive.Image(filename='cat_walker.jpg', width=0, height=0,
                          alt_text='The DJ Cat Walker popular among the Chinese'),
            archive.Options(content=[
                archive.OptionItem(
                    content=archive.Text('Option 1'),
                    is_key=True,
                    priority=0
                ),
                archive.OptionItem(
                    content=archive.Text('Option 2'),
                    is_key=False,
                    priority=0
                )
            ]),
            archive.Text("that's all")
        ],
        dimensions=[
            archive.Dimension('test quiz', 1),
            archive.Dimension('test item', 1)
        ]
    )])

    def test_should_archive(self):
        xml_bytes = self.sample_quiz_set.to_bytes()

        tree = ElementTree()
        tree.parse(source=BytesIO(xml_bytes))

        parsed = archive.QuizContainer.parse_xml_element(tree.getroot())
        self.assertEqual(parsed, self.sample_quiz_set)

    def test_builder(self):
        builder = archive.Builder(creation_time=self.sample_quiz_set.creation_time)
        builder.begin_quiz('Test quiz 1', creation_time=self.sample_quiz_set.content[0].creation_time) \
            .add_text('Hi I am text frame by test quiz 1') \
            .begin_image('The DJ Cat Walker popular among the Chinese') \
            .attach_image_file('cat_walker.jpg') \
            .end_image() \
            .begin_options() \
            .begin_option(is_key=True, priority=0) \
            .add_text('Option 1') \
            .end_option() \
            .begin_option(is_key=False, priority=0) \
            .add_text('Option 2') \
            .end_option() \
            .end_options() \
            .add_text("that's all") \
            .end_quiz()
        built = builder.build()
        self.assertEqual(built.content[0].frames, self.sample_quiz_set.content[0].frames)


if __name__ == '__main__':
    unittest.main()
