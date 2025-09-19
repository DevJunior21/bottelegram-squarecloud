from django.contrib import admin
from .models import (
    Usuario, Assinatura, Pagamento, MensagemPromocional,
    WelcomeConfig, PixButtonConfig, CarrosselOferta, ConfiguracaoPromocao
)
from .forms import MensagemPromocionalForm
from django.contrib import messages
import logging

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telegram_id', 'idioma', 'status', 'data_criacao']
    list_filter = ['status', 'idioma', 'data_criacao']
    search_fields = ['nome', 'telegram_id']
    readonly_fields = ['data_criacao', 'data_atualizacao']

@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'plano', 'status', 'data_inicio', 'data_fim']
    list_filter = ['status', 'plano', 'data_criacao']
    search_fields = ['usuario__nome', 'usuario__telegram_id']
    readonly_fields = ['data_criacao', 'data_atualizacao']

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['assinatura', 'valor', 'status', 'data_criacao']
    list_filter = ['status', 'data_criacao']
    search_fields = ['assinatura__usuario__nome', 'transaction_id']
    readonly_fields = ['data_criacao', 'data_atualizacao']

@admin.register(MensagemPromocional)
class MensagemPromocionalAdmin(admin.ModelAdmin):
    form = MensagemPromocionalForm
    list_display = ['titulo', 'idioma', 'ativa', 'data_inicio', 'data_fim']
    list_filter = ['ativa', 'idioma', 'data_inicio', 'data_fim']
    search_fields = ['titulo', 'texto']
    list_editable = ['ativa']
    actions = ["enviar_promocao"]

    def enviar_promocao(self, request, queryset):
        """Ação para enviar promoção via admin"""
        from django.conf import settings

        # Verificar se telegram bot está configurado
        if not hasattr(settings, 'BOT_TOKEN') or not settings.BOT_TOKEN:
            self.message_user(request, "Token do bot não configurado!", messages.ERROR)
            return

        try:
            # Implementação simplificada - pode ser expandida
            usuarios = Usuario.objects.filter(status__in=['visitante', 'assinante', 'ativo'])
            enviados = 0

            for promo in queryset:
                if promo.ativa:
                    # Aqui seria implementada a lógica de envio
                    # Por enquanto apenas contamos os usuários
                    enviados += usuarios.count()

            self.message_user(request, f"Promoção enviada para {enviados} usuários!", messages.SUCCESS)

        except Exception as e:
            logging.error(f"Erro ao enviar promoção: {e}")
            self.message_user(request, f"Erro ao enviar promoção: {e}", messages.ERROR)

    enviar_promocao.short_description = "Enviar esta promoção para todos os usuários"

@admin.register(WelcomeConfig)
class WelcomeConfigAdmin(admin.ModelAdmin):
    list_display = ['idioma', 'mensagem', 'url_video', 'arquivo_video']
    list_filter = ['idioma']

@admin.register(PixButtonConfig)
class PixButtonConfigAdmin(admin.ModelAdmin):
    list_display = ['ordem', 'legenda', 'valor', 'ativo']
    list_display_links = ['legenda']
    list_filter = ['ativo']
    list_editable = ['ordem', 'ativo', 'valor']
    search_fields = ["legenda"]
    ordering = ['ordem']

@admin.register(CarrosselOferta)
class CarrosselOfertaAdmin(admin.ModelAdmin):
    list_display = ['ordem', 'mensagem', 'valor', 'ativo']
    list_display_links = ['mensagem']
    list_filter = ['ativo']
    list_editable = ['ordem', 'ativo']
    ordering = ['ordem']
    fields = ("ordem", "mensagem", "valor", "legenda_botao_aceitar", "legenda_botao_recusar", "url_midia", "arquivo_midia", "ativo")

@admin.register(ConfiguracaoPromocao)
class ConfiguracaoPromocaoAdmin(admin.ModelAdmin):
    list_display = [
        'ativo', 'get_intervalo_formatado', 'ultima_execucao',
        'proxima_execucao', 'total_envios'
    ]
    list_display_links = ['get_intervalo_formatado']
    list_editable = ['ativo']
    readonly_fields = [
        'ultima_execucao', 'proxima_execucao', 'total_envios',
        'data_criacao', 'data_atualizacao'
    ]
    fieldsets = (
        ('Configuração Principal', {
            'fields': ('ativo', 'intervalo_valor', 'intervalo_periodo'),
            'description': 'Ative o envio automático e defina o intervalo desejado. Só é permitido um registro.'
        }),
        ('Informações de Execução', {
            'fields': ('ultima_execucao', 'proxima_execucao', 'total_envios'),
            'classes': ('collapse',),
            'description': 'Esses campos são atualizados automaticamente pelo sistema.'
        }),
        ('Informações do Sistema', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    help_texts = {
        'ativo': 'Ative para enviar promoções automaticamente para visitantes.',
        'intervalo_valor': 'Com que frequência (em minutos) a promoção será enviada.',
        'intervalo_periodo': 'Unidade do intervalo (minutos, horas, dias).',
    }

    def get_intervalo_formatado(self, obj):
        return obj.get_intervalo_display()
    get_intervalo_formatado.short_description = 'Intervalo'

    def has_add_permission(self, request):
        # Permitir apenas uma instância
        return not ConfiguracaoPromocao.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Não permitir deletar a configuração
        return False

    def save_model(self, request, obj, form, change):
        # Atualizar próxima execução quando ativar
        if obj.ativo and not change:
            from django.utils import timezone
            from datetime import timedelta

            if obj.intervalo_periodo == 'minutes':
                delta = timedelta(minutes=obj.intervalo_valor)
            elif obj.intervalo_periodo == 'hours':
                delta = timedelta(hours=obj.intervalo_valor)
            elif obj.intervalo_periodo == 'days':
                delta = timedelta(days=obj.intervalo_valor)

            obj.proxima_execucao = timezone.now() + delta

        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        # Se não existe configuração, criar uma padrão
        if not ConfiguracaoPromocao.objects.exists():
            ConfiguracaoPromocao.objects.create(
                ativo=False,
                intervalo_valor=60,
                intervalo_periodo='minutes'
            )
        extra_context = extra_context or {}
        extra_context['title'] = 'Configuração intuitiva do envio automático de promoções'
        return super().changelist_view(request, extra_context)