from django.shortcuts import render
from .models import NavMenuItem
from .image_processing import TransformImage


def home(response):
    menu_items = NavMenuItem.objects.all()
    target_resolution = (1366, 768)
    banner_resolution = (466, 69)
    header_image = TransformImage(image_path='main/static/building.jpg')
    header_image.set_target_resolution(target_resolution)
    header_image.set_banner_resolution(banner_resolution)
    header_image.rotate()
    header_image.resize()
    header_image.make_top_bar()
    return render(response, 'main/home.html', {'menu_items': menu_items,
                                               'top_bar_height': f"{header_image.image_out.size[1]}px",
                                               'content_margin': f"{header_image.image_out.size[1] + 20}px",
                                               'top_bar': header_image.image_out_path.split('/')[-1],
                                               'banner_height': header_image.logo_banner_resolution[1],
                                               'banner_width': header_image.logo_banner_resolution[0]
                                               }
                  )


def about_us(response):
    return render(response, 'main/about_us.html', {})


def aircraft_hangars(response):
    return render(response, 'main/aircraft_hangars.html', {})


def commercial_industrial(response):
    return render(response, 'main/commercial_industrial.html', {})


def farm_ranch(response):
    return render(response, 'main/farm_ranch.html', {})


def heritage_buildings(response):
    return render(response, 'main/heritage_buildings.html', {})


def storage_units(response):
    return render(response, 'main/storage_units.html', {})


def workshops(response):
    return render(response, 'main/workshops.html', {})


def clear_span(response):
    return render(response, 'main/clear_span_structure.html', {})


def multi_span(response):
    return render(response, 'main/multi_span_structure.html', {})


def cladding(response):
    return render(response, 'main/cladding.html', {})


def structural_sections(response):
    return render(response, 'main/structural_sections.html', {})


def doors(response):
    return render(response, 'main/doors.html', {})


def erection(response):
    return render(response, 'main/erection.html', {})


def glossary(response):
    return render(response, 'main/glossary.html', {})


def photos(response):
    return render(response, 'main/photos.html', {})


def contact(response):
    return render(response, 'main/contact.html', {})

