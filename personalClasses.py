from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
import random

from fpdf import FPDF
from datetime import date

class MultipleFormsMixin(FormMixin):


    form_classes = {}

    def get_form_classes(self):
        return self.form_classes

    def get_forms(self, form_classes):
        return dict([(key,klass(**self.get_form_kwargs())) for key, klass in form_classes.items()])

    def get_context_data(self, **kwargs):
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms()
        return super().get_context_data(**kwargs)

    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)

    def forms_invalid(self, forms) :
        return self.render_to_response(self.get_context_data(forms=forms))


class ProcessMultipleFormsView(ProcessFormView):

    def get(self, request, *args, **kwargs):
        forms_classes = self.get_form_classes()
        forms = self.get_forms(forms_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        forms_classes = self.get_form_classes()
        forms = self.get_forms(forms_classes)
        if all(form.is_valid() for form in forms.values()):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

class BaseMultipleFormsView(MultipleFormsMixin, ProcessMultipleFormsView):
    """
    A base view for displaying several forms.
    """

class MultipleFormsView(TemplateResponseMixin, BaseMultipleFormsView):
    """
    A  view for displaying several forms qnd rendering a template response.
    """

def random_phrases(objet) :
    sentences = [
        objet +' dans la maison!',
        'Hey '+ objet +'!',
        'Tranquille ou quoi '+ objet +'?',
        'Alors, qu\'est-ce qu\'on fait aujourd\'hui '+ objet +'?',
        'Bienvenue '+ objet,
        'Pfff... Encore toi '+ objet,
        'Content de te revoir '+ objet +'!',
        'S/O '+ objet +'!',
        'Ooh '+objet+', morale?',
        'Regardez qui est là? '+ objet + '!',
        'Et bien ' + objet + ', je t\'ai manqué?'

    ]
    return random.choice(sentences)

def generation(obj):
    customer = [
        obj['customer_identity'],
        obj['address'],
        obj['email'],
        obj['phone'],
        obj['payment'],
    ]
    site_datas = [
        obj['site_type'],
        obj['site_category'],
        obj['site_quantity'],
        obj['site_cost'],
    ]
    db_datas = [
        obj['db_exist'],
        obj['db_category'],
        obj['db_quantity'],
        obj['db_cost'],
    ]
    domain_datas = [
        obj['domain_exist'],
        obj['domain_extension'],
        obj['domain_period'],
        obj['domain_quantity'],
        obj['domain_cost'],
        
    ]
    hosting_datas = [
        obj['hosting_exist'],
        obj['hosting_type'],
        obj['hosting_period'],
        obj['hosting_quantity'],
        obj['hosting_cost'],
        
    ]
    maint_datas = [
        obj['maintenance_exist'],
        obj['maintenance_category'],
        obj['maintenance_quantity'],
        obj['maintenance_cost'],
        
    ]
    datas = [
        site_datas, db_datas, domain_datas, maint_datas, hosting_datas 
    ]

    # Orientation et unité de mesure
    page = FPDF("P", 'cm', 'A4')
    MY_STRINGS = {
        'date' : date.today(),
        'company_name' : 'STAR TECH GROUP',
        'invoice_no' : 'Devis#',
        'grandtotal' : 'Total Général',
        'special_note1' : 'Ce document fait office d"Annexe 1 tel que référencé dans le contrat de conception.'
    }

    # Codes Couleur
    # Bleu Ciel(3,196,249)

    ORDER_DATA = [
        datas[0],
        datas[1],
        ['Nom de domaine', datas[2][1]+'/'+datas[2][2], datas[2][3], datas[2][4]],
        ['Maintenance', datas[3][1], datas[3][2], datas[3][3]],
        ['Hebergement', datas[4][1]+'/'+datas[4][2], datas[4][3], datas[4][4]]
    ]

    # Calcul des prix totaux et total général
    general_total = 0
    for row in ORDER_DATA:
        subtotal = row[2] * row[3]
        row.append(subtotal)
        general_total += subtotal

    # Ajout de la page
    page.add_page()

    ### Début de la personalisation ###

    # Police par défaut et saut de page automatique
    page.set_font('arial','', 12)
    page.set_auto_page_break(True)

    ## En-tête du devis
    page.image('Star Tech/logo.png', x=1, y=1, w=2.5)
    page.set_xy(3.5, 1.7)
    page.set_font('times','B', 14)
    page.cell(txt=MY_STRINGS.get('company_name') ,w=page.get_string_width(MY_STRINGS.get('company_name'))+0.4 , h=1, align='C')

    page.set_xy(15,1.7)
    page.set_font('helvetica', 'B', 10)
    page.cell(txt='Devis no', w=0, h=0.7)
    page.set_xy(16.9, 1.7)
    page.set_font('helvetica', '', 10)
    page.cell(txt='002', w=0, h=0.7)

    page.set_xy(15,2.3)
    page.set_font('helvetica', 'B', 10)
    page.cell(txt='Date', w=0, h=0.7)
    page.set_xy(16.9, 2.3)
    page.set_font('helvetica', '', 10)
    page.cell(txt=str(MY_STRINGS['date']), w=0, h=0.7)

    ## Destinataire du devis
    page.set_xy(1, 5)
    page.cell(w=page.get_string_width('Destinataire :')+0.4, h=0.7,txt='Destinataire :', ln=True)

    page.set_font('helvetica', 'B', 10)
    page.cell(page.get_string_width(customer[0])+0.4, 0.7, customer[0], ln=True)

    page.set_font('helvetica', '', 9)
    page.set_text_color(105, 105, 105)
    page.cell(page.get_string_width(customer[1])+0.4, 0.7, customer[1], ln=True)
    page.cell(page.get_string_width(customer[3])+0.4, 0.7, customer[3], ln=True)

    page.ln(1.5)

    ## Tableau
    # En tête
    #page.set_xy()
    page.set_font('helvetica', 'B', 11)
    page.set_fill_color(3,196,249)
    page.set_text_color(255,255,255)
    page.cell(txt='Description'.upper(), w=8, h=1, fill=True)
    page.cell(txt='Type/Durée'.upper(), w=3, h=1, align='C', fill=True)
    page.cell(txt='quantité'.upper(), w=3, h=1, align='C', fill=True)
    page.cell(txt='prix'.upper(), w=3, h=1, align='C', fill=True)
    page.cell(txt='total'.upper(), w=3, h=1, align='C', ln=1, fill=True)

    # Contenu du tableau
    for row in ORDER_DATA:
        if ORDER_DATA.index(row)%2 == 0:
            page.set_fill_color(212, 208, 204)
            page.set_text_color(0,0,0)
            for cell in row:
                if row.index(cell) ==0:
                    page.set_font('helvetica', 'B', 9)
                    page.cell(8, 1, cell, fill=True, border="LR")
                elif row.index(cell) == 4:
                    page.set_font('helvetica', '', 9)
                    page.cell(2.9, 1, '$' + cell, border="LR", fill=True, align='C', ln=1)                       
                else:
                    page.set_font('helvetica', '', 9)
                    page.cell(3, 1,str(cell), border="LR", fill=True, align='C')
        else:
            for cell in row:
                if row.index(cell) ==0:
                    page.set_font('helvetica', 'B', 9)
                    page.cell(8, 1,cell, border="LR")
                elif row.index(cell) == 4:
                    page.set_font('helvetica', '', 9)
                    page.cell(2.9, 1, '$' + cell, border="LR", align='C', ln=1)                       
                else:
                    page.set_font('helvetica', '', 9)
                    page.cell(3, 1,str(cell), border="LR", align='C')
        page.ln()

    page.ln(0.7)



    ## Total
    page.set_x(13.5)
    page.set_font('helvetica', 'B', 10)
    page.cell(txt='Sous-total :', w=3, h=0.7)
    page.cell(w=4, h=0.7, txt= f'${general_total}', align='R', ln=True)

    #page.set_x(13.5)
    #page.set_font('helvetica', '', 9)
    #page.cell(4, 0.7, f'Remise {5}%')
    #page.cell(3, 0.7, f'- ${11.75}', align='R', ln=True)

    page.set_x(12.5)
    page.set_font('helvetica', 'B', 9)
    page.cell(w=8, h=0.7, txt='____________________________________________', ln=1)

    page.set_x(13.5)
    page.set_font('helvetica', 'B', 10)
    page.cell(txt='total général :'.upper(), w=3.5, h=0.7)
    page.cell(w=3.5, h=0.7, txt='$'+str(general_total), align='R')

    page.ln()


    ## Mode de paiement
    #page.set_xy()
    #page.set_font('helvetica', '', 11)
    page.cell(txt='Mode de Paiement', w=4, h=0.7, ln=1)

    page.set_font('helvetica', '', 9)
    page.set_text_color(105, 105, 105)
    page.cell(txt='Orange-Money', w=4, h=0.7, ln=1)
    page.cell(txt='UBA', w=4, h=0.7, ln=1)
    page.cell(txt='Cash', w=4, h=0.7, ln=1)

    page.ln(1.5)
    ## Contact et Signature

    # Contact 
    #page.set_xy()
    page.set_text_color(0, 0, 0)
    page.set_font('helvetica', 'B', 11)
    page.cell(txt='Contact', w=4, h=0.7, ln=1)

    page.set_font('helvetica', '', 9)
    page.set_text_color(105, 105, 105)
    page.cell(txt='+243 891 955 351', w=4, h=0.7, ln=1)
    page.cell(txt='lyonstartech@gmail.com', w=4, h=0.7, ln=1)
    page.set_font('helvetica', 'B', 9)
    page.set_text_color(0, 0, 0)
    page.cell(txt='www.star-techgroup.com', w=4, h=0.7)

    # Signature
    #page.image(name='',x='', y='')
    #page.cell()
    #page.set_x(13.5)
    #page.set_text_color(0, 0, 0)
    #page.set_font('helvetica', 'B', 11)
    #page.cell(txt='Christany ILUNGA',h=0.7, w=7, align='C' , ln=1)

    #page.set_x(13.5)
    #page.set_text_color(105, 105, 105)
    #page.set_font('helvetica', '', 9)
    #page.cell(txt='Directrice Finanncière',h=0.7, w=7, align='C')

    page.ln(2.5)


    ## Notes supplémentaires
    page.set_text_color(0, 0, 0)
    page.set_font('helvetica', 'B', 11)
    page.cell(txt='Note', w=4, h=0.7, ln=1)

    page.set_font('helvetica', '', 9)
    page.set_text_color(105, 105, 105)
    page.cell(txt=MY_STRINGS['special_note1'], w=page.get_string_width(MY_STRINGS['special_note1'])+0.5, h=0.7, ln=1)



    # Enregistrement du fichier
    page.output("Devis "+ customer[0] +".pdf")