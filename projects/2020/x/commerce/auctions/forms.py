from django import forms
from .models import Listing, Bid, Comments

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item_title', 'description', 'starting_bid', 'image', 'active', 'category']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']  
               
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        
        