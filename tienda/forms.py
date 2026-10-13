from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario rápido de alta de productos (panel de la Evaluación 1), ahora
    construido sobre el modelo Producto. Mantiene las validaciones de entrada:
    nombre de al menos 3 caracteres, precio mayor a 0 y stock no negativo.
    """
    stock = forms.IntegerField(
        label="Stock inicial (Casa Matriz)",
        min_value=0,
        initial=0,
        error_messages={"min_value": "El stock no puede ser negativo."},
    )

    class Meta:
        model = Producto
        fields = ["sku", "nombre", "categoria", "marca", "precio", "descripcion", "imagen"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}
        error_messages = {"precio": {"min_value": "El precio debe ser mayor a 0."}}

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre
