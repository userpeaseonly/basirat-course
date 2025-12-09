from django.core.management.base import BaseCommand
from django.utils.text import slugify
from courses.models import Course, Lesson, Material


class Command(BaseCommand):
    help = 'Populates database with test courses, lessons, and materials including tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing test data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing test data...'))
            Course.objects.filter(slug__in=['python-basics', 'web-development']).delete()
            self.stdout.write(self.style.SUCCESS('✓ Cleared existing test data'))

        self.stdout.write('Creating test data...')

        # Create Python course
        course, created = Course.objects.get_or_create(
            slug='python-basics',
            defaults={
                'title': 'Python Programming Basics',
                'summary': 'Learn Python fundamentals with interactive lessons and quizzes.',
                'is_published': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created course: {course.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course.title}'))

        # Lesson 1: Introduction
        lesson1, created = Lesson.objects.get_or_create(
            course=course,
            slug='introduction',
            defaults={
                'title': 'Introduction to Python',
                'description': 'Get started with Python programming',
                'order': 0,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson1.title}'))

            Material.objects.create(
                lesson=lesson1,
                title='What is Python?',
                material_type=Material.LEARNING,
                content='''Python is a high-level, interpreted programming language known for its simplicity and readability.

Key features:
- Easy to learn syntax
- Powerful standard library
- Cross-platform compatibility
- Large community support

Python is used for web development, data science, automation, and much more.''',
                order=0,
            )

            Material.objects.create(
                lesson=lesson1,
                title='Python History Video',
                material_type=Material.LEARNING,
                content='Watch this video to learn about the history of Python and why Guido van Rossum created it.',
                order=1,
                # Admin should upload video file manually to media/materials/
            )

            Material.objects.create(
                lesson=lesson1,
                title='Installing Python',
                material_type=Material.LEARNING,
                content='''To install Python:

1. Visit python.org
2. Download the latest version
3. Run the installer
4. Verify installation by typing: python --version

Make sure to check "Add Python to PATH" during installation.''',
                order=2,
            )

            Material.objects.create(
                lesson=lesson1,
                title='Python Installation Tutorial (Video)',
                material_type=Material.LEARNING,
                content='Step-by-step video guide for installing Python on Windows, Mac, and Linux.',
                order=3,
                # Admin uploads video
            )

            # Task: Single choice
            Material.objects.create(
                lesson=lesson1,
                title='Quiz: Python Basics',
                material_type=Material.TASK,
                question_type=Material.SINGLE_CHOICE,
                question_payload={
                    'question': 'What type of programming language is Python?',
                    'choices': [
                        'Compiled',
                        'Interpreted',
                        'Assembly',
                        'Machine code'
                    ],
                    'correct_answer': 'Interpreted'
                },
                order=4,
            )

            Material.objects.create(
                lesson=lesson1,
                title='Quiz: Python Creator',
                material_type=Material.TASK,
                question_type=Material.SINGLE_CHOICE,
                question_payload={
                    'question': 'Who created the Python programming language?',
                    'choices': [
                        'James Gosling',
                        'Guido van Rossum',
                        'Brendan Eich',
                        'Dennis Ritchie'
                    ],
                    'correct_answer': 'Guido van Rossum'
                },
                order=5,
            )

            self.stdout.write(self.style.SUCCESS(f'    ✓ Created 6 materials for {lesson1.title}'))

        # Lesson 2: Variables and Data Types
        lesson2, created = Lesson.objects.get_or_create(
            course=course,
            slug='variables-and-data-types',
            defaults={
                'title': 'Variables and Data Types',
                'description': 'Understanding Python variables and basic data types',
                'order': 1,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson2.title}'))

            Material.objects.create(
                lesson=lesson2,
                title='Python Variables',
                material_type=Material.LEARNING,
                content='''Variables in Python are containers for storing data values.

Example:
```python
name = "John"
age = 25
height = 5.9
is_student = True
```

Python is dynamically typed - you don't need to declare variable types.''',
                order=0,
            )

            Material.objects.create(
                lesson=lesson2,
                title='Variables Explained (Video)',
                material_type=Material.LEARNING,
                content='Visual explanation of how Python variables work in memory and how assignment differs from other languages.',
                order=1,
                # Admin uploads video
            )

            Material.objects.create(
                lesson=lesson2,
                title='Data Types Overview',
                material_type=Material.LEARNING,
                content='''Common Python data types:

1. **Strings (str)**: Text data - "Hello World"
2. **Integers (int)**: Whole numbers - 42
3. **Floats (float)**: Decimal numbers - 3.14
4. **Booleans (bool)**: True or False
5. **Lists**: Ordered collections - [1, 2, 3]
6. **Dictionaries**: Key-value pairs - {"name": "John"}
7. **Tuples**: Immutable sequences - (1, 2, 3)
8. **Sets**: Unordered unique collections - {1, 2, 3}

Use type() function to check data types.''',
                order=2,
            )

            Material.objects.create(
                lesson=lesson2,
                title='Working with Strings',
                material_type=Material.LEARNING,
                content='''String operations and methods:

**Concatenation:**
```python
first = "Hello"
last = "World"
full = first + " " + last
```

**Common methods:**
- `upper()` - Convert to uppercase
- `lower()` - Convert to lowercase
- `strip()` - Remove whitespace
- `split()` - Split into list
- `replace()` - Replace substring
- `find()` - Find substring position

**F-strings (formatted strings):**
```python
name = "Alice"
age = 30
message = f"My name is {name} and I am {age} years old"
```''',
                order=3,
            )

            Material.objects.create(
                lesson=lesson2,
                title='Data Types Tutorial (Video)',
                material_type=Material.LEARNING,
                content='Comprehensive video covering all Python data types with examples and use cases.',
                order=4,
                # Admin uploads video
            )

            # Task: Multiple choice
            Material.objects.create(
                lesson=lesson2,
                title='Quiz: Data Types',
                material_type=Material.TASK,
                question_type=Material.MULTI_CHOICE,
                question_payload={
                    'question': 'Which of the following are mutable data types in Python? (Select all that apply)',
                    'choices': [
                        'List',
                        'String',
                        'Dictionary',
                        'Tuple',
                        'Set'
                    ],
                    'correct_answer': ['List', 'Dictionary', 'Set']
                },
                order=5,
            )

            Material.objects.create(
                lesson=lesson2,
                title='Quiz: String Operations',
                material_type=Material.TASK,
                question_type=Material.SINGLE_CHOICE,
                question_payload={
                    'question': 'What does the following code output? print("Hello".upper())',
                    'choices': [
                        'hello',
                        'HELLO',
                        'Hello',
                        'hELLO'
                    ],
                    'correct_answer': 'HELLO'
                },
                order=6,
            )

            # Task: Free response
            Material.objects.create(
                lesson=lesson2,
                title='Exercise: Variable Assignment',
                material_type=Material.TASK,
                question_type=Material.FREE_RESPONSE,
                question_payload={
                    'question': '''Write Python code that creates three variables:
- A variable called `name` storing your name
- A variable called `age` storing your age
- A variable called `city` storing your city

Then print all three variables using an f-string in this format:
"My name is [name], I am [age] years old, and I live in [city]."'''
                },
                order=7,
            )

            self.stdout.write(self.style.SUCCESS(f'    ✓ Created 8 materials for {lesson2.title}'))

        # Lesson 3: Control Flow
        lesson3, created = Lesson.objects.get_or_create(
            course=course,
            slug='control-flow',
            defaults={
                'title': 'Control Flow and Conditionals',
                'description': 'Learn if statements, loops, and program flow control',
                'order': 2,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson3.title}'))

            Material.objects.create(
                lesson=lesson3,
                title='If Statements',
                material_type=Material.LEARNING,
                content='''Conditional statements allow you to execute code based on conditions.

Syntax:
```python
if condition:
    # code block
elif another_condition:
    # code block
else:
    # code block
```

Example:
```python
age = 18
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

**Comparison operators:**
- `==` Equal to
- `!=` Not equal to
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal''',
                order=0,
            )

            Material.objects.create(
                lesson=lesson3,
                title='Conditionals Tutorial (Video)',
                material_type=Material.LEARNING,
                content='Learn how to use if, elif, and else statements with practical examples and common patterns.',
                order=1,
                # Admin uploads video
            )

            Material.objects.create(
                lesson=lesson3,
                title='Loops in Python',
                material_type=Material.LEARNING,
                content='''Python has two main loop types:

**For loops** - Iterate over sequences:
```python
# Loop through range
for i in range(5):
    print(i)

# Loop through list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Loop through string
for char in "Python":
    print(char)
```

**While loops** - Repeat while condition is true:
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

**Loop control:**
- `break` - Exit loop completely
- `continue` - Skip to next iteration
- `pass` - Do nothing (placeholder)''',
                order=2,
            )

            Material.objects.create(
                lesson=lesson3,
                title='For and While Loops (Video)',
                material_type=Material.LEARNING,
                content='Visual demonstration of how loops work, including nested loops and loop control statements.',
                order=3,
                # Admin uploads video
            )

            Material.objects.create(
                lesson=lesson3,
                title='Logical Operators',
                material_type=Material.LEARNING,
                content='''Combine conditions using logical operators:

**and** - Both conditions must be True:
```python
age = 25
has_license = True
if age >= 18 and has_license:
    print("Can drive")
```

**or** - At least one condition must be True:
```python
is_weekend = True
is_holiday = False
if is_weekend or is_holiday:
    print("No work today!")
```

**not** - Negates a condition:
```python
is_raining = False
if not is_raining:
    print("Go outside")
```

**Order of precedence:** not > and > or''',
                order=4,
            )

            # Task: Single choice about loops
            Material.objects.create(
                lesson=lesson3,
                title='Quiz: Control Flow',
                material_type=Material.TASK,
                question_type=Material.SINGLE_CHOICE,
                question_payload={
                    'question': 'Which keyword is used to exit a loop prematurely?',
                    'choices': [
                        'exit',
                        'break',
                        'stop',
                        'return'
                    ],
                    'correct_answer': 'break'
                },
                order=5,
            )

            Material.objects.create(
                lesson=lesson3,
                title='Quiz: Logical Operators',
                material_type=Material.TASK,
                question_type=Material.MULTI_CHOICE,
                question_payload={
                    'question': 'Which statements will print "True"? (Select all that apply)',
                    'choices': [
                        'print(True and True)',
                        'print(True and False)',
                        'print(True or False)',
                        'print(False or False)',
                        'print(not False)'
                    ],
                    'correct_answer': ['print(True and True)', 'print(True or False)', 'print(not False)']
                },
                order=6,
            )

            # Task: Free response
            Material.objects.create(
                lesson=lesson3,
                title='Exercise: FizzBuzz',
                material_type=Material.TASK,
                question_type=Material.FREE_RESPONSE,
                question_payload={
                    'question': '''Write a Python program that prints numbers from 1 to 15.
For multiples of 3, print "Fizz" instead of the number.
For multiples of 5, print "Buzz" instead of the number.
For multiples of both 3 and 5, print "FizzBuzz".

Example output:
1
2
Fizz
4
Buzz
Fizz
7
...'''
                },
                order=7,
            )

            Material.objects.create(
                lesson=lesson3,
                title='Exercise: Number Guessing',
                material_type=Material.TASK,
                question_type=Material.FREE_RESPONSE,
                question_payload={
                    'question': '''Create a simple number guessing game:
1. Set a secret number (e.g., 7)
2. Ask the user to guess
3. Use a while loop to keep asking until they guess correctly
4. Give hints like "Too high" or "Too low"
5. Congratulate them when they guess correctly

Hint: Use input() to get user input and int() to convert to integer.'''
                },
                order=8,
            )

            self.stdout.write(self.style.SUCCESS(f'    ✓ Created 9 materials for {lesson3.title}'))

        # Lesson 4: Functions
        lesson4, created = Lesson.objects.get_or_create(
            course=course,
            slug='functions',
            defaults={
                'title': 'Functions and Code Reusability',
                'description': 'Learn how to write reusable code with functions',
                'order': 3,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {lesson4.title}'))

            Material.objects.create(
                lesson=lesson4,
                title='Introduction to Functions',
                material_type=Material.LEARNING,
                content='''Functions are reusable blocks of code that perform specific tasks.

**Defining a function:**
```python
def greet(name):
    print(f"Hello, {name}!")

# Calling the function
greet("Alice")
```

**Return values:**
```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

**Benefits of functions:**
- Code reusability
- Better organization
- Easier testing
- Reduce redundancy''',
                order=0,
            )

            Material.objects.create(
                lesson=lesson4,
                title='Functions Explained (Video)',
                material_type=Material.LEARNING,
                content='Complete guide to Python functions including parameters, return values, and scope.',
                order=1,
            )

            Material.objects.create(
                lesson=lesson4,
                title='Function Parameters',
                material_type=Material.LEARNING,
                content='''Different ways to pass parameters:

**Positional arguments:**
```python
def introduce(name, age):
    print(f"I'm {name} and I'm {age}")

introduce("Bob", 25)
```

**Keyword arguments:**
```python
introduce(age=25, name="Bob")
```

**Default parameters:**
```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")  # Hello, Alice!
greet("Bob", "Hi")  # Hi, Bob!
```

**Variable arguments:**
```python
def sum_all(*numbers):
    return sum(numbers)

print(sum_all(1, 2, 3, 4))  # 10
```''',
                order=2,
            )

            Material.objects.create(
                lesson=lesson4,
                title='Quiz: Functions',
                material_type=Material.TASK,
                question_type=Material.SINGLE_CHOICE,
                question_payload={
                    'question': 'What keyword is used to send a value back from a function?',
                    'choices': [
                        'give',
                        'return',
                        'send',
                        'output'
                    ],
                    'correct_answer': 'return'
                },
                order=3,
            )

            Material.objects.create(
                lesson=lesson4,
                title='Exercise: Calculator Function',
                material_type=Material.TASK,
                question_type=Material.FREE_RESPONSE,
                question_payload={
                    'question': '''Create a calculator function that takes three parameters:
- Two numbers (num1, num2)
- An operation ('+', '-', '*', '/')

The function should return the result of the operation.

Example:
calculate(10, 5, '+') should return 15
calculate(10, 5, '*') should return 50'''
                },
                order=4,
            )

            self.stdout.write(self.style.SUCCESS(f'    ✓ Created 5 materials for {lesson4.title}'))

        # Add Web Development course
        web_course, created = Course.objects.get_or_create(
            slug='web-development',
            defaults={
                'title': 'Introduction to Web Development',
                'summary': 'Learn HTML, CSS, and JavaScript basics to build your first website.',
                'is_published': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created course: {web_course.title}'))

            web_lesson1, _ = Lesson.objects.get_or_create(
                course=web_course,
                slug='html-basics',
                defaults={
                    'title': 'HTML Fundamentals',
                    'description': 'Learn the building blocks of web pages',
                    'order': 0,
                }
            )

            Material.objects.create(
                lesson=web_lesson1,
                title='What is HTML?',
                material_type=Material.LEARNING,
                content='''HTML (HyperText Markup Language) is the standard language for creating web pages.

**Basic structure:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
</head>
<body>
    <h1>Hello World</h1>
    <p>This is a paragraph.</p>
</body>
</html>
```

HTML uses tags to structure content.''',
                order=0,
            )

            Material.objects.create(
                lesson=web_lesson1,
                title='HTML Tutorial (Video)',
                material_type=Material.LEARNING,
                content='Complete HTML tutorial covering tags, attributes, and semantic HTML.',
                order=1,
            )

            Material.objects.create(
                lesson=web_lesson1,
                title='Quiz: HTML Basics',
                material_type=Material.TASK,
                question_type=Material.SINGLE_CHOICE,
                question_payload={
                    'question': 'What does HTML stand for?',
                    'choices': [
                        'Hyper Text Markup Language',
                        'High Tech Modern Language',
                        'Home Tool Markup Language',
                        'Hyperlinks and Text Markup Language'
                    ],
                    'correct_answer': 'Hyper Text Markup Language'
                },
                order=2,
            )

            self.stdout.write(self.style.SUCCESS(f'  ✓ Created lesson: {web_lesson1.title} with 3 materials'))

        self.stdout.write(self.style.SUCCESS('\n✓ Test data population complete!'))
        self.stdout.write(self.style.SUCCESS(f'Courses created: {Course.objects.filter(slug__in=["python-basics", "web-development"]).count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total lessons: {Lesson.objects.filter(course__slug__in=["python-basics", "web-development"]).count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total materials: {Material.objects.filter(lesson__course__slug__in=["python-basics", "web-development"]).count()}'))
