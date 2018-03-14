from django.db import models


class ContractType(models.Model):
    """
    Tipul contractului: Asigurare credit
    """
    id = models.AutoField(primary_key=True)
    contract_type = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.contract_type


class ContractStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.status


class Contract(models.Model):
    """
    Model for a contract.
    """

    id = models.AutoField(primary_key=True)
    contract_type = models.ForeignKey(ContractType,on_delete=models.SET_NULL,null=True)
    company_name = models.CharField(max_length=200,null=False,blank=False)
    name = models.CharField(max_length=200,default="Nume contract",null=False,blank=False)
    contract_id = models.CharField(max_length=200,null=False,blank=False)
    start_date = models.DateField(verbose_name="Data semnaturii")
    end_date = models.DateField(name="Data rezilierii",null=True,blank=True)
    payment = models.FloatField(null=True,blank=True)
    comment = models.TextField(name="Comentariu",null=True,blank=True)
    pdf_contract = models.FileField(null=True,blank=True)
    status = models.ForeignKey(ContractStatus,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name + "_" + self.contract_id

