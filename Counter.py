#examples taken from here: http://stackoverflow.com/a/1750187
mydoclist = ['Julie loves me more than Linda loves me',
             'Jane likes me more than Julie loves me',
             'He likes basketball more than baseball']

# mydoclist = ['sun sky bright', 'sun su
from collections import Counter

for doc in mydoclist:
    tf = Counter()
    for word in doc.split():
        tf[word] += 1
    print
    tf.items()