from faker import Faker
from jinja2 import Environment, FileSystemLoader
import pdfkit

fake = Faker()
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('cv_template.html')

for i in range(50):  # Generate 50 CVs
    data = {
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'education': fake.job(),
        'experience': fake.text(max_nb_chars=300),
        'skills': ', '.join(fake.words(5))
    }
    html = template.render(data)
    pdfkit.from_string(html, f'output/cv_{i}.pdf')
