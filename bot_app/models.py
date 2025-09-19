from django.db import models

class Usuario(models.Model):
    IDIOMA_CHOICES = [
        ('pt', 'Português'),
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
    ]
    telegram_id = models.BigIntegerField(unique=True)
    nome = models.CharField(max_length=255)
    idioma = models.CharField(max_length=2, choices=IDIOMA_CHOICES, default='pt')
    status = models.CharField(max_length=50, default='visitante', choices=[
        ('visitante', 'Visitante'),
        ('assinante', 'Assinante'),
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ])
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ultima_promocao_id = models.IntegerField(null=True, blank=True)
    link_enviado = models.BooleanField(default=False, help_text="Indica se o link de convite foi enviado")
    data_envio_link = models.DateTimeField(null=True, blank=True, help_text="Data/hora em que o link foi enviado")

    def __str__(self):
        return f"{self.nome} ({self.telegram_id})"

class Assinatura(models.Model):
    PLANO_CHOICES = [
        ('1_dia', '1 Dia'),
        ('diario', 'Diário'),
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
        ('vitalicia', 'Vitalícia'),
        ('30 dias', '30 dias'),
        ('90 dias', '90 dias'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('ativa', 'Ativa'),
        ('expirada', 'Expirada'),
        ('cancelada', 'Cancelada'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plano = models.CharField(max_length=50, choices=PLANO_CHOICES)
    status = models.CharField(max_length=50, default='pendente', choices=STATUS_CHOICES)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario} - {self.plano} ({self.status})"

    def is_active(self):
        from django.utils import timezone
        return self.status == 'ativa' and (self.data_fim is None or self.data_fim > timezone.now())

class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
        ('falha', 'Falha'),
    ]
    assinatura = models.ForeignKey(Assinatura, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='pendente', choices=STATUS_CHOICES)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    pix_qr_code = models.TextField(null=True, blank=True)
    pix_copia_cola = models.TextField(null=True, blank=True)
    pushinpay_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assinatura} - {self.valor} ({self.status})"

class MensagemPromocional(models.Model):
    IDIOMA_CHOICES = [
        ('pt', 'Português'),
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
    ]
    idioma = models.CharField(max_length=2, choices=IDIOMA_CHOICES, default='pt')
    titulo = models.CharField(max_length=100)
    texto = models.TextField()
    url_video = models.URLField(blank=True, null=True)
    arquivo_video = models.FileField(upload_to='promocoes/videos/', blank=True, null=True)
    ativa = models.BooleanField(default=True)
    data_inicio = models.DateTimeField(blank=True, null=True)
    data_fim = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class WelcomeConfig(models.Model):
    IDIOMA_CHOICES = [
        ('pt', 'Português'),
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
    ]
    idioma = models.CharField("Idioma", max_length=2, choices=IDIOMA_CHOICES, default='pt')
    mensagem = models.TextField("Mensagem de boas-vindas", blank=True, null=True)
    url_video = models.URLField("URL do vídeo de boas-vindas", blank=True, null=True)
    arquivo_video = models.FileField("Arquivo de vídeo de boas-vindas", upload_to='welcome/videos/', blank=True, null=True)

    def __str__(self):
        return f"Configuração de Boas-vindas ({self.idioma})"

class PixButtonConfig(models.Model):
    ordem = models.PositiveIntegerField("Ordem de exibição", default=0, help_text="Ordem em que o botão aparecerá (menor número = primeiro)")
    valor = models.DecimalField("Valor do botão", max_digits=10, decimal_places=2)
    legenda = models.CharField("Legenda do botão", max_length=100)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.legenda} - R$ {self.valor}"

class CarrosselOferta(models.Model):
    ordem = models.PositiveIntegerField("Ordem no carrossel")
    mensagem = models.TextField("Mensagem da oferta")
    valor = models.DecimalField("Valor adicional", max_digits=10, decimal_places=2)
    legenda_botao_aceitar = models.CharField("Legenda do botão aceitar", max_length=100)
    legenda_botao_recusar = models.CharField("Legenda do botão recusar", max_length=100)
    url_midia = models.URLField("URL da mídia", blank=True, null=True)
    arquivo_midia = models.FileField("Arquivo de mídia", upload_to='carrossel/ofertas/', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem"]

    def __str__(self):
        return f"Oferta {self.ordem}: {self.mensagem[:30]}..."

class ConfiguracaoPromocao(models.Model):
    INTERVALO_CHOICES = [
        (1, '1 minuto'),
        (5, '5 minutos'),
        (10, '10 minutos'),
        (15, '15 minutos'),
        (30, '30 minutos'),
        (60, '60 minutos (1 hora)'),
        (120, '120 minutos (2 horas)'),
        (180, '180 minutos (3 horas)'),
        (360, '360 minutos (6 horas)'),
        (720, '720 minutos (12 horas)'),
        (1440, '1440 minutos (1 dia)'),
    ]
    PERIODO_CHOICES = [
        ('minutes', 'Minutos'),
        ('hours', 'Horas'),
        ('days', 'Dias'),
    ]
    ativo = models.BooleanField(
        "Ativar envio automático de promoções",
        default=False,
        help_text="Ative para enviar promoções automaticamente para visitantes."
    )
    intervalo_valor = models.IntegerField(
        "Intervalo em minutos",
        choices=INTERVALO_CHOICES,
        default=60,
        help_text="Intervalo entre envios em MINUTOS (60 = 1 hora, 120 = 2 horas, etc)."
    )
    intervalo_periodo = models.CharField(
        "Período do intervalo",
        max_length=10,
        choices=PERIODO_CHOICES,
        default='minutes',
        help_text="SEMPRE deixe em 'Minutos' - o valor acima já está em minutos."
    )
    ultima_execucao = models.DateTimeField("Última execução", null=True, blank=True)
    proxima_execucao = models.DateTimeField("Próxima execução", null=True, blank=True)
    total_envios = models.IntegerField("Total de envios realizados", default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração de Promoção"
        verbose_name_plural = "Configurações de Promoção"

    def __str__(self):
        status = "Ativo" if self.ativo else "Inativo"
        return f"Promoções Automáticas - {status}"

    def save(self, *args, **kwargs):
        # Garante que só exista uma instância
        if not self.pk and ConfiguracaoPromocao.objects.exists():
            raise Exception("Só pode existir uma configuração de promoção automática!")
        super().save(*args, **kwargs)

    def get_intervalo_display(self):
        """Retorna o intervalo formatado para exibição"""
        if self.intervalo_valor == 60:
            return "60 minutos (1 hora)"
        elif self.intervalo_valor == 120:
            return "120 minutos (2 horas)"
        elif self.intervalo_valor == 180:
            return "180 minutos (3 horas)"
        elif self.intervalo_valor == 360:
            return "360 minutos (6 horas)"
        elif self.intervalo_valor == 720:
            return "720 minutos (12 horas)"
        elif self.intervalo_valor == 1440:
            return "1440 minutos (1 dia)"
        else:
            return f"{self.intervalo_valor} minutos"