from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(CodeBlockPreprocessor(md), 'code_block', 25)

class CodeBlockPreprocessor(Preprocessor):
    RE = re.compile(r'```(\w+):([\w./\s-]+?)\n([\s\S]*?)\n```', re.DOTALL)

    def run(self, lines):
        new_text = []
        text = '\n'.join(lines)

        def repl(match):
            lang = match.group(1)
            label = match.group(2).strip()
            code = match.group(3).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            return f'<div class="code-container"><div class="code-filename">{label}</div><pre><code class="language-{lang}">{code}</code></pre></div>'
        
        text = self.RE.sub(repl, text)
        new_text = text.split('\n')
        return new_text

def makeExtension(**kwargs):
    return CodeBlockExtension(**kwargs)
