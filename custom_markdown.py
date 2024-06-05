from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(CodeBlockPreprocessor(md), 'code_block', 25)

class CodeBlockPreprocessor(Preprocessor):
    RE = re.compile(r'```(\w+):([\w.\s]+)\n(.*?)```', re.DOTALL)

    def run(self, lines):
        new_text = []
        text = '\n'.join(lines)

        for match in self.RE.finditer(text):
            lang = match.group(1)
            filename = match.group(2).strip()
            code = match.group(3)
            replacement = f'<pre><code class="language-{lang}"><div class="code-filename">{filename}</div>{code}</code></pre>'
            text = text.replace(match.group(0), replacement)
        
        new_text = text.split('\n')
        return new_text
