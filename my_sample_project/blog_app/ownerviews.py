from django.views.generic import DeleteView, UpdateView, CreateView

class OwnerDeleteView(DeleteView):
    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset
    
class OwnerCreateView(CreateView):
    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)
    

class OwnerUpdateView(UpdateView):
    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset