import importlib, traceback, inspect, sys
import os

path = 'chatbot/message_parser.py'
print('--- Reading file:', path)
with open(path, 'r', encoding='utf-8') as f:
    src = f.read()
print('Length:', len(src))
print('\n--- CWD and directory listing')
print('cwd:', os.getcwd())
print('listing chatbot/:', os.listdir('chatbot'))
print('file size via os.stat:', os.stat(path).st_size)
print('\nHead (first 400 chars):\n')
print(src[:400])
print('\n--- Attempting import of chatbot.message_parser')
try:
    # Ensure project root is on sys.path so package imports resolve
    project_root = os.getcwd()
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    if 'chatbot.message_parser' in sys.modules:
        print('Removing existing module from sys.modules to force re-import')
        del sys.modules['chatbot.message_parser']
    m = importlib.import_module('chatbot.message_parser')
    print('Imported module file:', getattr(m, '__file__', None))
    names = [n for n in dir(m) if not n.startswith('__')]
    print('Public names in module:', names)
    if 'MessageParser' in names:
        print('\nMessageParser is present. Source:')
        print(inspect.getsource(m.MessageParser))
    else:
        print('\nMessageParser NOT found in module names.')
except Exception:
    print('\nException during import:')
    traceback.print_exc()

print('\n--- sys.modules keys containing chatbot:')
for k in sorted(k for k in sys.modules.keys() if k.startswith('chatbot')):
    print(k)
