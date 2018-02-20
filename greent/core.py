import json
from greent.clinical import Clinical
from greent.endotype import Endotype
from greent.ontologies.disease_ont import DiseaseOntology
from greent.ontologies.go import GO
from greent.ontologies.hpo import HPO
from greent.ontologies.mondo import Mondo
from greent.services.biolink import Biolink
from greent.services.chembio import ChemBioKS
from greent.services.chemotext import Chemotext
from greent.services.ctd import CTD
from greent.services.hetio import HetIO
from greent.services.hgnc import HGNC
from greent.services.oxo import OXO
from greent.services.pharos import Pharos
from greent.services.quickgo import QuickGo
from greent.service import ServiceContext
from greent.services.tkba import TranslatorKnowledgeBeaconAggregator
from greent.services.uberongraph import UberonGraphKS
from greent.services.unichem import UniChem
from greent.translator import Translator
from greent.transreg import TranslatorRegistry
from greent.util import LoggingUtil

logger = LoggingUtil.init_logging (__file__)

class GreenT:

    ''' The Green Translator API - a single Python interface aggregating access mechanisms for 
    all Green Translator services. '''

    def __init__(self, config=None, override={}):
        self.service_context = ServiceContext.create_context (config)
        service_context = self.service_context
        
        self.clinical = Clinical (service_context)
        #temporarly taken out because of http errors
        #self.exposures = CMAQ (service_context)
        self.endotype = Endotype (service_context)

        self.chembio = ChemBioKS (self.service_context)
        self.chemotext = Chemotext (self.service_context)
        self.disease_ontology = DiseaseOntology (self.service_context)
        self.pharos = Pharos (self.service_context)
        self.oxo = OXO (self.service_context)
        self.hpo = HPO (self.service_context)
        self.hetio = HetIO (self.service_context)
        self.biolink = Biolink (self.service_context)
        self.mondo = Mondo(self.service_context)
        self.go = GO(self.service_context)
        self.tkba = TranslatorKnowledgeBeaconAggregator (self.service_context)
        self.translator_registry = TranslatorRegistry (self.service_context)
        self.quickgo = QuickGo (self.service_context)
        self.translator = Translator (core=self)
        self.hgnc = HGNC(self.service_context)
        self.uberongraph = UberonGraphKS(self.service_context)
        self.ctd = CTD(self.service_context)
        self.unichem = UniChem(self.service_context)

    # Exposure API
    def get_exposure_scores (self, exposure_type, start_date, end_date, exposure_point):
        return self.exposures.get_scores (
            exposure_type = exposure_type,
            start_date    = start_date,
            end_date      = end_date,
            lat_lon       = exposure_point)

    def get_exposure_values (self, exposure_type, start_date, end_date, exposure_point):
        return self.exposures.get_values (
            exposure_type  = exposure_type,
            start_date     = start_date,
            end_date       = end_date,
            lat_lon        = exposure_point)

    # ChemBio API
    def get_exposure_conditions_json (self, chemicals):
        return json.dumps (self.get_exposure_conditions (chemicals))

    def get_exposure_conditions (self, chemicals):
        return self.chembio.get_exposure_conditions (chemicals)

    def get_drugs_by_condition_json (self, conditions):
        return json.dumps (self.get_drugs_by_condition (conditions))

    def get_drugs_by_condition (self, conditions):
        return self.chembio.get_drugs_by_condition (conditions)

    def get_genes_pathways_by_disease_json (self, diseases):
        return json.dumps (self.get_genes_pathways_by_disease (diseases))

    def get_genes_pathways_by_disease (self, diseases):
        return self.chembio.get_genes_pathways_by_disease (diseases)

    def get_drug_gene_disease (self, disease_name, drug_name):
        return self.chembio.get_drug_gene_disease (disease_name, drug_name)
    
    # Clinical API
    def get_patients (self, age=None, sex=None, race=None, location=None):
        return self.clinical.get_patients (age, sex, race, location)

    def execute (self, request):
        return self.translator.translate_chain (request)
