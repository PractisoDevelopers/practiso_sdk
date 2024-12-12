import unittest
from io import BytesIO
from xml.etree.ElementTree import ElementTree

import practiso_sdk.archive as archive


class ArchiveTestCase(unittest.TestCase):
    sample_quiz_set = archive.QuizContainer(content=[archive.Quiz(
        name='Test quiz 1',
        frames=[
            archive.Text('Hi I am text frame by test quiz 1'),
            archive.Image(filename='cat_walker.jpg', width=400, height=295,
                          alt_text='The DJ Cat Walker popular among the Chinese'),
            archive.Options(content=[
                archive.OptionItem(
                    content=archive.Text('Option 1'),
                    is_key=True,
                    priority=0
                ),
                archive.OptionItem(
                    content=archive.Text('Option 2'),
                    is_key=True,
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


if __name__ == '__main__':
    unittest.main()
