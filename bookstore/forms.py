from bookstore.models import Book
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import Book, Genre, Author
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Hidden, Button, HTML, Div, Field, Row, Fieldset


class BookForm(forms.ModelForm):
    class Meta: 
        model = Book
        fields = '__all__'
        
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Save', 'Save', css_class='btn-primary'))

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "bookform"
        
        #Create a new folder select list, with added css and style codes
        genre = Div('genre', css_class="col-xs-12", style="padding:0px;") 
        self.helper.layout.pop(6) #remove the original folder select list 
        #Insert new folder select list with a "Create New Folder" button as a Fieldset
        self.helper.layout.insert(6,Fieldset("Select genre",genre, Button("creategenremodal", value="Add New Genre", css_class="btn btn-primary btn-sm col-xs-12 ", data_toggle="modal", data_target="#myModal")))
        
        #Create a new tag multi-select list, with added css and style codes
        author = Div('author',css_class = "col-xs-12", style="padding:0px;") 
        oldtagselect = self.helper.layout.pop(7) #remove the original tag multi-select list
        #Insert new tag multi-select list with a "Create New Tag" button as a Fieldset
        self.helper.layout.insert(7, Fieldset("Select Author",author, Button("createauthormodal", value="Add New Author", css_class="btn btn-primary btn-sm col-xs-12", data_toggle="modal", data_target="#myModal2")))
        
        #Create a "Create New Note" button 
        self.helper.layout.append(Submit('btn_addbook', 'Add Book', css_class='addbook', style="margin-top:15px;"))
        #Add a hidden field 'btn_createnote' so that it will be submitted together in the form to allow server side to 'know'
        #that this button has been clicked
        self.helper.layout.append(Hidden(name='btn_addbook', value="btn_addbook"))
        
        
        
    def full_clean(self):
        #http://stackoverflow.com/questions/4340287/override-data-validation-on-one-django-form-element
        super(BookForm, self).full_clean()
        if 'tag' in self._errors:
            self.cleaned_data['tag'] = []
            print("remove tag errors")
            del self._errors['tag']
            
            
            
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "genreform"
        self.helper.layout.append(Hidden(name='btn_creategenre', value="btn_creategenre"))
        self.helper.layout.append(Submit('btn_creategenre', 'Add Genre', css_class='creategenre', data_dismiss="modal"))
  

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

        
    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "authorform"
        self.helper.layout.append(Hidden(name='btn_createauthor', value="btn_createauthor"))
        self.helper.layout.append(Submit('btn_createauthor', 'Add Author', css_class='createauthor', data_dismiss="modal"))


