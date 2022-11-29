from main.models import NavMenuItem

menu_items = {'About Us': {'is_dropdown': False, 'dropdown': None, 'url': 'about_us.html'},
              'Building Structures': {'is_dropdown': True, 'dropdown': None, 'url': None},
              'Aircraft Hangars': {'is_dropdown': False, 'dropdown': 'Building Structures', 'url': 'aircraft_hangars.html'},
              'Commercial/Industrial': {'is_dropdown': False, 'dropdown': 'Building Structures', 'url': 'commercial_industrial.html'},
              'Farm & Ranch': {'is_dropdown': False, 'dropdown': 'Building Structures', 'url': 'farm_ranch.html'},
              'Heritage Buildings': {'is_dropdown': False, 'dropdown': 'Building Structures', 'url': 'heritage_buildings.html'},
              'Storage Units': {'is_dropdown': False, 'dropdown': 'Building Structures', 'url': 'storage_units.html'},
              'Workshops': {'is_dropdown': False, 'dropdown': 'Building Structures', 'url': 'workshops.html'},
              'Products': {'is_dropdown': True, 'dropdown': None, 'url': None},
              'Clear Span Structures': {'is_dropdown': False, 'dropdown': 'Products', 'url': 'clear_span_structures.html'},
              'Multi Span Structures': {'is_dropdown': False, 'dropdown': 'Products', 'url': 'multi_span_structures.html'},
              'Cladding': {'is_dropdown': False, 'dropdown': 'Products', 'url': 'cladding.html'},
              'Structural Sections': {'is_dropdown': False, 'dropdown': 'Products', 'url': 'structural_sections.html'},
              'Doors': {'is_dropdown': False, 'dropdown': 'Products', 'url': 'doors.html'},
              'Erection': {'is_dropdown': False, 'dropdown': None, 'url': 'erection.html'},
              'Glossary': {'is_dropdown': False, 'dropdown': None, 'url': 'glossary.html'},
              'Photos': {'is_dropdown': False, 'dropdown': None, 'url': 'photos.html'},
              'Contact Us': {'is_dropdown': False, 'dropdown': None, 'url': 'contact.html'},
              }


if __name__ == '__main__':
    for item, info in menu_items.items():
        i = NavMenuItem(text=item, url=info['url'], is_dropdown=info['is_dropdown'], dropdown=info['dropdown'])
        i.save()
