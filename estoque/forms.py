from django import forms
from django.core.exceptions import ValidationError
from .models import Movimentacao, Categoria, Produto
import re

from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    lembrar_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

# Função auxiliar para calcular o dígito verificador
def calcular_digito(cpf, peso):
    soma = 0
    for i, n in enumerate(cpf):
        soma += int(n) * peso[i]
    resto = soma % 11
    return '0' if resto < 2 else str(11 - resto)

def is_cpf_valido(cpf):
    # Remove tudo que não for número
    cpf = re.sub(r'\D', '', cpf)

    # Verifica tamanho e se todos os números são iguais (ex: 111.111.111-11)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    # Caso de teste
    if cpf.count(cpf[0]) == 11:
        return True

    # Validação do 1º Dígito
    peso1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    primeiro_digito = calcular_digito(cpf[:9], peso1)
    if cpf[9] != primeiro_digito:
        return False

    # Validação do 2º Dígito
    peso2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    segundo_digito = calcular_digito(cpf[:10], peso2)
    if cpf[10] != segundo_digito:
        return False

    return True

class MovimentacaoForm(forms.ModelForm):
    # Campo "virtual" de categoria para filtro
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Selecione uma Categoria",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Movimentacao
        fields = ['tipo', 'categoria', 'produto', 'quantidade', 'observacao', 'solicitante_nome', 'solicitante_cpf']
        
        widgets = {
            # MUDANÇA AQUI: Alteramos para RadioSelect
            'tipo': forms.RadioSelect(attrs={'class': 'btn-check'}), 
            
            'produto': forms.Select(attrs={'class': 'form-select', 'disabled': 'true'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'solicitante_nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Quem vai receber o item? (Opcional)'
            }),
            'solicitante_cpf': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cpf', 'placeholder': '000.000.000-00', 'maxlength': '14'}),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Ex: Compra NF 123 ou Ajuste de Estoque'
            }),
        }
        labels = {
            'solicitante_nome': 'Destinatário / Solicitante',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['solicitante_nome'].required = False
        self.fields['produto'].queryset = Produto.objects.all().order_by('nome')

    def clean_solicitante_cpf(self):
        cpf_original = self.cleaned_data.get('solicitante_cpf')
        
        # Se o CPF for opcional e estiver vazio, retorna vazio (sem erro)
        if not cpf_original:
            return None
            
        # Remove caracteres para validar
        cpf_limpo = re.sub(r'\D', '', cpf_original)
        
        if not is_cpf_valido(cpf_limpo):
            raise ValidationError("CPF inválido. Verifique os números digitados.")
            
        return cpf_limpo # Retorna o CPF limpo (apenas números) para o banco
    
class SaidaRapidaForm(forms.ModelForm):
    # Campo "virtual" de categoria para filtro
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Selecione uma Categoria",
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )

    class Meta:
        model = Movimentacao
        # Adicionamos 'tipo', 'solicitante_nome' e 'solicitante_cpf'
        fields = ['tipo', 'categoria', 'produto', 'quantidade', 'solicitante_nome', 'solicitante_cpf']
        
        widgets = {
            # Widget de Radio para o Tipo (igual ao form completo)
            'tipo': forms.RadioSelect(attrs={'class': 'btn-check'}),
            
            'produto': forms.Select(attrs={'class': 'form-select form-select-lg', 'disabled': 'true'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control form-control-lg text-center', 'inputmode': 'numeric'}),
            
            # Widgets para os detalhes (Admin)
            'solicitante_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Solicitante'}),
            'solicitante_cpf': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cpf_rapido', 'placeholder': '000.000.000-00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.all().order_by('nome')
        
        # IMPORTANTE: Definir como não obrigatórios, pois o usuário comum não os preenche
        self.fields['tipo'].required = False
        self.fields['solicitante_nome'].required = False
        self.fields['solicitante_cpf'].required = False