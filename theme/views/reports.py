# coding=utf-8
"""
Created on 2020, May 24th
@author: orion
"""
# from PIL import Image

import io
import time

from django.shortcuts import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, Spacer, Image
from reportlab.lib.units import mm, cm

from theme.models import Theme, TropicalConfiguration
from theme.tasks.loading import get_context_graphics

SIZE_SPACER = 0.5*cm
STYLES = getSampleStyleSheet()
NORMAL_STYLE = STYLES["Normal"]
TITLE_STYLE = STYLES["Title"]
HEADING_STYLE = STYLES['Heading3']

FONT_SIZE = 10

COLOR_BOX_TMP = colors.white
COLOR_INNERGRID_TMP = colors.white
SIZE_ROW_TAB = [0.5*cm]
SIZE_SPACER = 0.5*cm

COL_SIZE_1 = 500
COL_SIZE_2 = COL_SIZE_1/2
COL_SIZE_3 = COL_SIZE_1/3
COL_SIZE_4 = COL_SIZE_1/4
COL_SIZE_5 = COL_SIZE_1/5
COL_SIZE_6 = COL_SIZE_1/6

COL_CARAC_1 = 100
COL_CARAC_2 = COL_CARAC_1/2
COL_CARAC_3 = COL_CARAC_1/3
COL_CARAC_4 = COL_CARAC_1/4
COL_CARAC_5 = COL_CARAC_1/5
COL_CARAC_6 = COL_CARAC_1/6


class NumberedCanvas(canvas.Canvas):
    """
    Classe de création du canevas du document
    """

    def __init__(self, *args, **kwargs):
        """
        constructeur de la classe
        """
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        """
        Visualisation de la page
        """
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """adds header and footer to the document"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header()
            self.draw_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header(self):
        """
        Affichage d'un entête
        """
        header_string = "AstrologiesLab"
        self.drawString(10 * mm, self._pagesize[1] - 10 * mm, header_string)
        string_width = self.stringWidth(header_string)
        self.line(15 * mm + string_width, self._pagesize[1] - 9 * mm,
                  self._pagesize[0] - 10 * mm, self._pagesize[1] - 9 * mm)

    def draw_footer(self, page_count):
        """
        Affichage d'un pied de page
        """
        self.line(10 * mm, 14 * mm, self._pagesize[0] - 10 * mm, 14 * mm)
        self.drawString(10 * mm, 10 * mm, time.strftime("%d/%m/%Y"))
        self.drawCentredString(self._pagesize[0] / 2, 10 * mm,
                               "Page %d / %d" % (self._pageNumber, page_count))


def get_images(request, theme):

    images = []

    image_width = 18 * cm

    if request.user.is_authenticated:
        profile = request.user.profile

        context = get_context_graphics(
            theme,
            configuration_tropical=profile.configuration_tropical,
            configuration_sidereal=profile.configuration_sidereal,
            json=False,
        )
    else:
        configuration = TropicalConfiguration.objects.filter(default=True)[0]

        context = get_context_graphics(theme, configuration_tropical=configuration, json=False)

    if context['show']['tropical']:

        fig = context['graphics']['tropical']

        width = fig['layout']['width']
        height = fig['layout']['height']

        image_ratio = height / width

        img_bytes = fig.to_image(format="png")
        img_file = io.BytesIO(img_bytes)

        images.append(
            Image(img_file, width=image_width, height=image_width * image_ratio),
        )

    if context['show']['sidereal']:

        fig = context['graphics']['sidereal']

        width = fig['layout']['width']
        height = fig['layout']['height']

        image_ratio = height / width

        img_bytes = fig.to_image(format="png")
        img_file = io.BytesIO(img_bytes)

        images.append(
            Image(img_file, width=image_width, height=image_width * image_ratio),
        )

    if context['show']['compounded']:

        fig = context['graphics']['compounded']

        width = fig['layout']['width']
        height = fig['layout']['height']

        image_ratio = height / width

        img_bytes = fig.to_image(format="png")
        img_file = io.BytesIO(img_bytes)

        images.append(
            Image(img_file, width=image_width, height=image_width * image_ratio),
        )

    return images


def generate_pdf(request, theme_id):

    theme = Theme.objects.get(id=theme_id)

    # Create a file-like buffer to receive PDF data.

    buffer = io.BytesIO()

    filename = 'theme.pdf'
    spacer = Spacer(1, SIZE_SPACER)
    doc = SimpleDocTemplate(
        buffer,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )
    contents = []

    # PERSON

    theme_data = [
        [Paragraph("<b>THÈME NATAL</b>", NORMAL_STYLE)],
        ['Prénom', theme.first_name],
        ['Nom', theme.last_name],
        ['Information supplémentaire', theme.further_information],
    ]
    theme_table = Table(
        theme_data,
    )
    contents.append(theme_table)
    contents.append(spacer)

    # DATE

    theme_data = [
        [Paragraph("<center><h6>Naissance</h6></center>", NORMAL_STYLE)],
        [
            'Date', "{} (heure locale)".format(
                theme.date,
            ),
        ],
        ['Ville', theme.location.city],
        ['Latitude', theme.location.latitude],
        ['Longitude', theme.location.longitude],
        ['Altitude', theme.location.altitude],
        ['Contexte', theme.location.context],
        ['Fuseau horaire', theme.location.time_zone],
    ]
    theme_table = Table(
        theme_data,
    )
    contents.append(theme_table)
    contents.append(spacer)

    # graphics
    images = get_images(request, theme)
    for image in images:
        contents.append(image)
        contents.append(spacer)

    # # LOCATION
    #
    # theme_data = [
    #     ['Ville', theme.location.city],
    #     ['Latitude', theme.location.latitude],
    #     ['Longitude', theme.location.longitude],
    #     ['Altitude', theme.location.altitude],
    #     ['Contexte', theme.location.context],
    #     ['Fuseau horaire', theme.location.time_zone],
    # ]
    #
    # theme_table = Table(
    #     theme_data,
    # )
    # contents.append(theme_table)
    # contents.append(spacer)

    doc.build(contents, canvasmaker=NumberedCanvas)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response.write(buffer.getvalue())
    buffer.close()

    return response
