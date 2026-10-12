"""
Full Standalone Corporate Registry Generator
Generates comprehensive multi-jurisdictional corporate structures with realistic data
No external dependencies beyond Python standard library
"""

import json
import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum
import uuid
from abc import ABC, abstractmethod


# ==================== ENUMERATIONS ====================

class JurisdictionType(Enum):
    US_FEDERAL = "US_FEDERAL"
    US_STATE = "US_STATE"
    UK = "UK"
    CAYMAN_ISLANDS = "CAYMAN_ISLANDS"
    LUXEMBOURG = "LUXEMBOURG"
    SINGAPORE = "SINGAPORE"
    UAE = "UAE"
    HONG_KONG = "HONG_KONG"
    BVI = "BVI"
    MALTA = "MALTA"


class EntityType(Enum):
    CORPORATION = "CORPORATION"
    LLC = "LLC"
    PARTNERSHIP = "PARTNERSHIP"
    TRUST = "TRUST"
    FOUNDATION = "FOUNDATION"
    HOLDING_COMPANY = "HOLDING_COMPANY"
    SUBSIDIARY = "SUBSIDIARY"
    SPECIAL_PURPOSE_VEHICLE = "SPECIAL_PURPOSE_VEHICLE"
    BRANCH = "BRANCH"
    INVESTMENT_FUND = "INVESTMENT_FUND"
    JOINT_VENTURE = "JOINT_VENTURE"


class OwnershipType(Enum):
    DIRECT = "DIRECT"
    INDIRECT = "INDIRECT"
    BENEFICIAL = "BENEFICIAL"
    NOMINEE = "NOMINEE"
    TRUSTEE = "TRUSTEE"


class DocumentType(Enum):
    ARTICLES_OF_INCORPORATION = "ARTICLES_OF_INCORPORATION"
    BYLAWS = "BYLAWS"
    OPERATING_AGREEMENT = "OPERATING_AGREEMENT"
    CERTIFICATE_OF_GOOD_STANDING = "CERTIFICATE_OF_GOOD_STANDING"
    BOARD_RESOLUTION = "BOARD_RESOLUTION"
    MINUTES_OF_MEETING = "MINUTES_OF_MEETING"
    DIRECTORS_REGISTER = "DIRECTORS_REGISTER"
    SHAREHOLDERS_REGISTER = "SHAREHOLDERS_REGISTER"
    BENEFICIAL_OWNERSHIP_REGISTER = "BENEFICIAL_OWNERSHIP_REGISTER"
    TRUST_DEED = "TRUST_DEED"
    UBO_DECLARATION = "UBO_DECLARATION"
    COMPLIANCE_CERTIFICATE = "COMPLIANCE_CERTIFICATE"


# ==================== DATA CLASSES ====================

@dataclass
class Person:
    """Individual person record"""
    person_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str = ""
    last_name: str = ""
    middle_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    nationality: str = ""
    passport_number: Optional[str] = None
    id_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    residential_address: str = ""
    business_address: Optional[str] = None
    kyc_status: str = "PENDING"
    kyc_date: Optional[str] = None
    pep_status: bool = False
    sanctions_status: bool = False
    
    def get_full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Shareholder:
    """Shareholder record"""
    shareholder_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: Optional[str] = None
    person_id: Optional[str] = None
    shares_issued: int = 0
    share_class: str = "COMMON"
    percentage_ownership: float = 0.0
    voting_rights: float = 0.0
    acquisition_date: str = ""
    is_beneficial_owner: bool = False
    
    def is_individual(self) -> bool:
        return self.person_id is not None
    
    def is_entity(self) -> bool:
        return self.entity_id is not None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Director:
    """Director/Officer record"""
    director_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    person_id: str = ""
    title: str = ""
    appointment_date: str = ""
    resignation_date: Optional[str] = None
    is_active: bool = True
    responsibilities: List[str] = field(default_factory=list)
    signature_authority: bool = False
    compensation: Optional[float] = None
    
    def is_current(self) -> bool:
        return self.is_active and self.resignation_date is None
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ControlChain:
    """Represents indirect control through intermediary entities"""
    chain_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_entity_id: str = ""
    to_entity_id: str = ""
    path: List[str] = field(default_factory=list)
    percentage_ownership: float = 0.0
    control_type: str = "INDIRECT"
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_depth(self) -> int:
        return len(self.path) - 2 if len(self.path) > 1 else 0
    
    def is_circular(self) -> bool:
        return len(self.path) != len(set(self.path))
    
    def to_dict(self) -> Dict:
        d = asdict(self)
        d['control_type'] = self.control_type
        return d


@dataclass
class CorporateDocument:
    """Corporate document record"""
    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str = ""
    document_type: str = "ARTICLES_OF_INCORPORATION"
    jurisdiction: str = "US_FEDERAL"
    issue_date: str = ""
    effective_date: str = ""
    expiry_date: Optional[str] = None
    file_path: str = ""
    document_hash: Optional[str] = None
    signatory_persons: List[str] = field(default_factory=list)
    approval_status: str = "DRAFT"
    compliance_verified: bool = False
    metadata: Dict = field(default_factory=dict)
    content_summary: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CorporateEntity:
    """Corporate entity record"""
    entity_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    legal_name: str = ""
    entity_type: str = "CORPORATION"
    jurisdiction: str = "US_FEDERAL"
    state_province: Optional[str] = None
    registration_number: str = ""
    registration_date: str = ""
    dissolution_date: Optional[str] = None
    tax_id: str = ""
    business_address: str = ""
    registered_agent: Optional[str] = None
    fiscal_year_end: str = "12/31"
    active_status: bool = True
    
    # Structural relationships
    parent_entity_id: Optional[str] = None
    subsidiary_entity_ids: List[str] = field(default_factory=list)
    related_entity_ids: List[str] = field(default_factory=list)
    
    # Stakeholders
    shareholders: List[Shareholder] = field(default_factory=list)
    directors: List[Director] = field(default_factory=list)
    authorized_signatories: List[str] = field(default_factory=list)
    
    # Control information
    control_chains: List[ControlChain] = field(default_factory=list)
    beneficial_owners: List[str] = field(default_factory=list)
    
    # Documents
    corporate_documents: List[CorporateDocument] = field(default_factory=list)
    
    # Compliance
    kyc_status: str = "PENDING"
    kyc_completion_date: Optional[str] = None
    last_audit_date: Optional[str] = None
    compliance_notes: str = ""
    
    def get_active_directors(self) -> List[Director]:
        return [d for d in self.directors if d.is_current()]
    
    def get_total_capitalization(self) -> float:
        return sum(sh.percentage_ownership for sh in self.shareholders)
    
    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "legal_name": self.legal_name,
            "entity_type": self.entity_type,
            "jurisdiction": self.jurisdiction,
            "registration_number": self.registration_number,
            "tax_id": self.tax_id,
            "active_status": self.active_status,
            "kyc_status": self.kyc_status,
            "shareholders_count": len(self.shareholders),
            "directors_count": len(self.directors),
            "subsidiary_count": len(self.subsidiary_entity_ids)
        }


# ==================== REALISTIC DATA GENERATOR ====================

class RealisticDataGenerator:
    """Generates realistic synthetic data"""
    
    FIRST_NAMES = {
        'US': ['John', 'Sarah', 'Michael', 'Jennifer', 'Robert', 'Emily', 'James', 'Mary', 'David', 'Lisa'],
        'UK': ['William', 'Lucy', 'Oliver', 'Amelia', 'George', 'Sophie', 'Harry', 'Olivia', 'Thomas', 'Emma'],
        'Singapore': ['Wei', 'Li', 'Chen', 'Lim', 'Tan', 'Wong', 'Ng', 'Koh', 'Lim', 'Chua'],
        'Hong Kong': ['Zhang', 'Liu', 'Wang', 'Li', 'Yang', 'Huang', 'Zhao', 'Wu', 'Guo', 'He'],
        'UAE': ['Mohammed', 'Ahmed', 'Fatima', 'Aisha', 'Hassan', 'Layla', 'Omar', 'Noor', 'Zainab', 'Karim'],
        'Luxembourg': ['Jean', 'Marie', 'Pierre', 'Anne', 'Jacques', 'Sophie', 'Michel', 'Isabelle', 'Paul', 'Claire'],
        'Malta': ['Angelo', 'Maria', 'Joseph', 'Francesca', 'Paul', 'Theresa', 'Antonio', 'Camilla', 'Vincent', 'Mariella'],
        'Cayman Islands': ['James', 'Patricia', 'Michael', 'Jennifer', 'David', 'Margaret', 'Richard', 'Susan', 'Joseph', 'Jessica'],
        'BVI': ['Thomas', 'Barbara', 'Charles', 'Karen', 'Daniel', 'Nancy', 'Matthew', 'Lisa', 'Mark', 'Sandra'],
    }
    
    LAST_NAMES = {
        'US': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'],
        'UK': ['Thompson', 'Bennett', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Peterson', 'Hughes', 'Myers'],
        'Singapore': ['Ong', 'Lee', 'Chua', 'Lau', 'Quek', 'Yap', 'Soh', 'Pang', 'Lim', 'Seah'],
        'Hong Kong': ['Chan', 'Wong', 'Leung', 'Cheng', 'Tang', 'Kwok', 'Poon', 'Tam', 'Tse', 'Yeung'],
        'UAE': ['Al Maktoum', 'Al Nahyan', 'Al Qassimi', 'Al Mansoori', 'Al Mutawa', 'Al Suwaidi', 'Al Mazrouei', 'Al Ketbi'],
        'Luxembourg': ['Muller', 'Schmidt', 'Wagner', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Schulz', 'Hoffmann', 'Schroeder'],
        'Malta': ['Vella', 'Grech', 'Schembri', 'Azzopardi', 'Micallef', 'Camilleri', 'Galea', 'Zammit', 'Bonello', 'Aquilina'],
        'Cayman Islands': ['Taylor', 'Anderson', 'Thomas', 'Moore', 'Jackson', 'Martin', 'Perry', 'Patel', 'Young', 'King'],
        'BVI': ['Harper', 'Fuller', 'Austin', 'Mendez', 'Graham', 'Sullivan', 'Wallace', 'Pierce', 'Berry', 'Barker'],
    }
    
    COMPANY_PREFIXES = [
        'Global', 'International', 'Premier', 'Alliance', 'Capital', 'Equity', 'Strategic', 'Vertex',
        'Apex', 'Zenith', 'Meridian', 'Nexus', 'Quantum', 'Trinity', 'Vanguard', 'Paramount',
        'Imperial', 'Royal', 'Elite', 'Exclusive', 'Ascent', 'Pinnacle', 'Velocity', 'Synergy'
    ]
    
    COMPANY_SECTORS = [
        'Technology', 'Finance', 'Real Estate', 'Energy', 'Healthcare', 'Manufacturing',
        'Retail', 'Logistics', 'Media', 'Telecommunications', 'Consulting', 'Venture'
    ]
    
    COMPANY_SUFFIXES = [
        'Holdings', 'Investment', 'Partners', 'Group', 'Solutions', 'Ventures', 'Corporation',
        'Management', 'Enterprises', 'Finance', 'Capital', 'Assets', 'Services', 'Advisors', 'Trust', 'Fund'
    ]
    
    TITLES = ['CEO', 'CFO', 'COO', 'CTO', 'President', 'Vice President', 'Director',
              'Executive Director', 'Chairman', 'Treasurer', 'Secretary', 'General Counsel']
    
    @staticmethod
    def generate_person(nationality: str = 'US') -> Person:
        """Generate realistic person"""
        first_names = RealisticDataGenerator.FIRST_NAMES.get(nationality, RealisticDataGenerator.FIRST_NAMES['US'])
        last_names = RealisticDataGenerator.LAST_NAMES.get(nationality, RealisticDataGenerator.LAST_NAMES['US'])
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        middle_name = random.choice(first_names) if random.random() > 0.6 else None
        
        # Birth date
        birth_year = random.randint(1960, 1995)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        dob = f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d}"
        
        # Address
        if nationality == 'US':
            states = ['NY', 'CA', 'TX', 'FL', 'IL', 'PA', 'OH', 'MI', 'DE', 'MA']
            state = random.choice(states)
            cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Boston', 'Seattle']
            city = random.choice(cities)
            residential = f"{random.randint(100, 5000)} {random.choice(['Main', 'Oak', 'Park', 'Washington'])} St, {city}, {state} {random.randint(10000, 99999)}"
        elif nationality == 'UK':
            residential = f"{random.randint(100, 5000)} {random.choice(['High', 'Bond', 'Oxford', 'Fleet'])} Street, London, {random.choice(['SW1', 'W1', 'EC1', 'N1'])} {random.randint(1, 9)}{random.choice('ABCDEFGH')}"
        else:
            residential = f"{random.randint(100, 5000)} {random.choice(['Central', 'Main', 'Victoria'])} {random.choice(['Avenue', 'Street', 'Road'])}"
        
        kyc_status = random.choice(['VERIFIED', 'VERIFIED', 'VERIFIED', 'PENDING'])
        kyc_date = (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat() if kyc_status == 'VERIFIED' else None
        
        return Person(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_of_birth=dob,
            nationality=nationality,
            passport_number=f"{nationality[:2].upper()}{random.randint(10000000, 99999999)}",
            id_number=f"{random.randint(100000000, 999999999)}",
            email=f"{first_name.lower()}.{last_name.lower()}@{random.choice(['corporate.com', 'business.net', 'group.io'])}",
            phone=f"+{random.randint(1, 65)}{random.randint(10000000, 999999999)}",
            residential_address=residential,
            kyc_status=kyc_status,
            kyc_date=kyc_date,
            pep_status=random.random() < 0.05,
            sanctions_status=False
        )
    
    @staticmethod
    def generate_company_name() -> str:
        prefix = random.choice(RealisticDataGenerator.COMPANY_PREFIXES)
        sector = random.choice(RealisticDataGenerator.COMPANY_SECTORS)
        suffix = random.choice(RealisticDataGenerator.COMPANY_SUFFIXES)
        return f"{prefix} {sector} {suffix}"
    
    @staticmethod
    def generate_tax_id(jurisdiction: str) -> str:
        if jurisdiction == "US_FEDERAL":
            return f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"
        elif jurisdiction == "US_STATE":
            return f"EIN{random.randint(10000000, 99999999)}"
        elif jurisdiction == "UK":
            return f"{random.randint(100000000, 999999999)}"
        elif jurisdiction == "SINGAPORE":
            return f"{random.randint(100000000, 999999999)}"
        else:
            return f"TAX{random.randint(1000000, 9999999)}"
    
    @staticmethod
    def generate_registration_number(jurisdiction: str) -> str:
        prefixes = {
            "US_STATE": "",
            "US_FEDERAL": "FED",
            "UK": "",
            "CAYMAN_ISLANDS": "C",
            "SINGAPORE": "",
            "HONG_KONG": "HK",
            "LUXEMBOURG": "LUX",
            "BVI": "BVI",
            "UAE": "UAE",
            "MALTA": "MT"
        }
        prefix = prefixes.get(jurisdiction, "")
        return f"{prefix}{random.randint(1000000, 9999999)}"
    
    @staticmethod
    def get_jurisdiction_address(jurisdiction: str) -> str:
        addresses = {
            "US_STATE": f"{random.randint(100, 5000)} Delaware Ave, Wilmington, DE {random.randint(10000, 19999)}",
            "US_FEDERAL": f"{random.randint(100, 5000)} Wall Street, New York, NY {random.randint(10000, 19999)}",
            "UK": f"{random.randint(100, 5000)} {random.choice(['Canary', 'Broadgate', 'Lombard'])} Street, London EC2",
            "CAYMAN_ISLANDS": f"{random.randint(100, 5000)} Cayman Business Park, George Town, KY1-1108",
            "LUXEMBOURG": f"{random.randint(100, 5000)} rue de la Toison d'Or, Luxembourg City L-2113",
            "SINGAPORE": f"{random.randint(100, 5000)} Marina Bay, Singapore {random.randint(100000, 999999)}",
            "UAE": f"{random.randint(100, 5000)} Business Bay, Dubai, UAE",
            "HONG_KONG": f"{random.randint(100, 5000)} Central, Hong Kong",
            "BVI": f"{random.randint(100, 5000)} Main Street, Road Town, Tortola",
            "MALTA": f"{random.randint(100, 5000)} Valletta, Malta VLT 1000"
        }
        return addresses.get(jurisdiction, "International Business Address")


# ==================== CORPORATE STRUCTURE GRAPH ====================

class CorporateStructureGraph:
    """Manages complex corporate structure"""
    
    def __init__(self):
        self.entities: Dict[str, CorporateEntity] = {}
        self.persons: Dict[str, Person] = {}
        self.documents: Dict[str, CorporateDocument] = {}
        self.control_chains: Dict[str, ControlChain] = {}
    
    def add_entity(self, entity: CorporateEntity):
        self.entities[entity.entity_id] = entity
    
    def add_person(self, person: Person):
        self.persons[person.person_id] = person
    
    def add_document(self, document: CorporateDocument):
        self.documents[document.document_id] = document
        if document.entity_id in self.entities:
            self.entities[document.entity_id].corporate_documents.append(document)
    
    def add_control_chain(self, chain: ControlChain):
        self.control_chains[chain.chain_id] = chain
    
    def get_ownership_hierarchy(self, entity_id: str) -> Dict:
        """Get ownership hierarchy for entity"""
        if entity_id not in self.entities:
            return {}
        
        entity = self.entities[entity_id]
        hierarchy = {
            "entity": entity.to_dict(),
            "shareholders": [],
            "directors": [],
            "beneficial_owners": [],
            "control_chains": []
        }
        
        # Direct shareholders
        for shareholder in entity.shareholders:
            sh_info = {
                "shareholder_id": shareholder.shareholder_id,
                "percentage": shareholder.percentage_ownership,
                "type": "INDIVIDUAL" if shareholder.is_individual() else "ENTITY"
            }
            if shareholder.person_id and shareholder.person_id in self.persons:
                person = self.persons[shareholder.person_id]
                sh_info["name"] = person.get_full_name()
            elif shareholder.entity_id and shareholder.entity_id in self.entities:
                sh_info["name"] = self.entities[shareholder.entity_id].legal_name
            
            hierarchy["shareholders"].append(sh_info)
        
        # Directors
        for director in entity.directors:
            if director.person_id in self.persons:
                person = self.persons[director.person_id]
                hierarchy["directors"].append({
                    "name": person.get_full_name(),
                    "title": director.title,
                    "active": director.is_active,
                    "signature_authority": director.signature_authority
                })
        
        # Beneficial owners
        for ubo_id in entity.beneficial_owners:
            if ubo_id in self.persons:
                person = self.persons[ubo_id]
                hierarchy["beneficial_owners"].append({
                    "name": person.get_full_name(),
                    "kyc_status": person.kyc_status,
                    "pep": person.pep_status
                })
        
        # Control chains
        for chain in entity.control_chains:
            hierarchy["control_chains"].append({
                "depth": chain.get_depth(),
                "percentage": chain.percentage_ownership,
                "path_length": len(chain.path)
            })
        
        return hierarchy
    
    def verify_control_chain_integrity(self) -> List[str]:
        """Verify control chain integrity"""
        issues = []
        
        for chain_id, chain in self.control_chains.items():
            if chain.is_circular():
                issues.append(f"Circular control chain: {chain_id}")
            
            for entity_id in chain.path:
                if entity_id not in self.entities:
                    issues.append(f"Missing entity {entity_id} in chain {chain_id}")
            
            if chain.percentage_ownership < 0 or chain.percentage_ownership > 100:
                issues.append(f"Invalid ownership percentage in chain {chain_id}")
        
        return issues
    
    def get_multi_jurisdiction_summary(self) -> Dict:
        """Summarize across jurisdictions"""
        summary = {}
        
        for entity in self.entities.values():
            juris = entity.jurisdiction
            if juris not in summary:
                summary[juris] = {
                    "entity_count": 0,
                    "entities": [],
                    "total_subsidiaries": 0,
                    "kyc_verified": 0,
                    "kyc_pending": 0
                }
            
            summary[juris]["entity_count"] += 1
            summary[juris]["entities"].append(entity.legal_name)
            summary[juris]["total_subsidiaries"] += len(entity.subsidiary_entity_ids)
            
            if entity.kyc_status == "VERIFIED":
                summary[juris]["kyc_verified"] += 1
            else:
                summary[juris]["kyc_pending"] += 1
        
        return summary


# ==================== REGISTRY GENERATOR ====================

class CorporateRegistryGenerator:
    """Generates complete corporate registry"""
    
    def __init__(self):
        self.structure = CorporateStructureGraph()
        self.data_gen = RealisticDataGenerator()
    
    def generate_multi_level_holding_structure(self,
                                              num_holding_companies: int = 2,
                                              num_subsidiaries_per_holding: int = 3,
                                              num_sub_subsidiaries: int = 2) -> CorporateStructureGraph:
        """Generate multi-level holding structure"""
        
        # Create ultimate beneficial owners
        ultimate_owners = []
        for _ in range(random.randint(2, 4)):
            person = self.data_gen.generate_person(nationality=random.choice(['US', 'UK', 'Singapore']))
            self.structure.add_person(person)
            ultimate_owners.append(person)
        
        # Create holding companies in tax jurisdictions
        holding_companies = []
        holding_jurisdictions = ["CAYMAN_ISLANDS", "BVI", "LUXEMBOURG"]
        
        for i in range(num_holding_companies):
            jurisdiction = holding_jurisdictions[i % len(holding_jurisdictions)]
            
            holding = CorporateEntity(
                legal_name=self.data_gen.generate_company_name(),
                entity_type="HOLDING_COMPANY",
                jurisdiction=jurisdiction,
                registration_number=self.data_gen.generate_registration_number(jurisdiction),
                registration_date=(datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d'),
                tax_id=self.data_gen.generate_tax_id(jurisdiction),
                business_address=self.data_gen.get_jurisdiction_address(jurisdiction),
                kyc_status="VERIFIED"
            )
            
            # Distribute ownership
            ownership_percentages = self._distribute_ownership(len(ultimate_owners))
            for owner, percentage in zip(ultimate_owners, ownership_percentages):
                shareholder = Shareholder(
                    person_id=owner.person_id,
                    shares_issued=int(percentage * 10),
                    percentage_ownership=percentage,
                    is_beneficial_owner=True,
                    acquisition_date=holding.registration_date
                )
                holding.shareholders.append(shareholder)
            
            holding.beneficial_owners = [owner.person_id for owner in ultimate_owners]
            self.structure.add_entity(holding)
            holding_companies.append(holding)
        
        # Create operating subsidiaries
        operating_jurisdictions = ["US_STATE", "UK", "SINGAPORE", "HONG_KONG"]
        
        for holding in holding_companies:
            for j in range(num_subsidiaries_per_holding):
                jurisdiction = random.choice(operating_jurisdictions)
                
                operating = CorporateEntity(
                    legal_name=self.data_gen.generate_company_name(),
                    entity_type=random.choice(["CORPORATION", "LLC", "SUBSIDIARY"]),
                    jurisdiction=jurisdiction,
                    state_province="Delaware" if jurisdiction == "US_STATE" else None,
                    registration_number=self.data_gen.generate_registration_number(jurisdiction),
                    registration_date=(datetime.now() - timedelta(days=random.randint(200, 1095))).strftime('%Y-%m-%d'),
                    tax_id=self.data_gen.generate_tax_id(jurisdiction),
                    business_address=self.data_gen.get_jurisdiction_address(jurisdiction),
                    parent_entity_id=holding.entity_id,
                    kyc_status="VERIFIED"
                )
                
                # Holding company as shareholder
                shareholder = Shareholder(
                    entity_id=holding.entity_id,
                    shares_issued=1000,
                    percentage_ownership=100.0,
                    is_beneficial_owner=False,
                    acquisition_date=operating.registration_date
                )
                operating.shareholders.append(shareholder)
                
                # Control chain
                control_chain = ControlChain(
                    from_entity_id=holding.entity_id,
                    to_entity_id=operating.entity_id,
                    path=[holding.entity_id, operating.entity_id],
                    percentage_ownership=100.0,
                    control_type="INDIRECT"
                )
                self.structure.add_control_chain(control_chain)
                
                # Add directors
                for _ in range(random.randint(2, 4)):
                    director_person = self.data_gen.generate_person()
                    self.structure.add_person(director_person)
                    
                    director = Director(
                        person_id=director_person.person_id,
                        title=random.choice(self.data_gen.TITLES),
                        appointment_date=operating.registration_date,
                        is_active=True,
                        signature_authority=random.random() > 0.3
                    )
                    operating.directors.append(director)
                
                holding.subsidiary_entity_ids.append(operating.entity_id)
                self.structure.add_entity(operating)
                
                # Create sub-subsidiaries
                for k in range(num_sub_subsidiaries):
                    sub_jurisdiction = random.choice(["SINGAPORE", "HONG_KONG", "UK"])
                    
                    sub_sub = CorporateEntity(
                        legal_name=self.data_gen.generate_company_name(),
                        entity_type=random.choice(["SUBSIDIARY", "SPECIAL_PURPOSE_VEHICLE"]),
                        jurisdiction=sub_jurisdiction,
                        registration_number=self.data_gen.generate_registration_number(sub_jurisdiction),
                        registration_date=(datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                        tax_id=self.data_gen.generate_tax_id(sub_jurisdiction),
                        business_address=self.data_gen.get_jurisdiction_address(sub_jurisdiction),
                        parent_entity_id=operating.entity_id,
                        kyc_status="VERIFIED"
                    )
                    
                    shareholder = Shareholder(
                        entity_id=operating.entity_id,
                        shares_issued=500,
                        percentage_ownership=100.0,
                        is_beneficial_owner=False,
                        acquisition_date=sub_sub.registration_date
                    )
                    sub_sub.shareholders.append(shareholder)
                    
                    # Multi-level control chain
                    multi_chain = ControlChain(
                        from_entity_id=holding.entity_id,
                        to_entity_id=sub_sub.entity_id,
                        path=[holding.entity_id, operating.entity_id, sub_sub.entity_id],
                        percentage_ownership=100.0,
                        control_type="INDIRECT"
                    )
                    self.structure.add_control_chain(multi_chain)
                    
                    operating.subsidiary_entity_ids.append(sub_sub.entity_id)
                    self.structure.add_entity(sub_sub)
        
        # Generate documents
        self._generate_corporate_documents()
        
        return self.structure
    
    def _distribute_ownership(self, num_owners: int) -> List[float]:
        """Distribute ownership percentages"""
        if num_owners == 1:
            return [100.0]
        elif num_owners == 2:
            split = random.uniform(40, 60)
            return [split, 100.0 - split]
        else:
            base = 100.0 / num_owners
            percentages = [base + random.uniform(-base * 0.3, base * 0.3) for _ in range(num_owners)]
            total = sum(percentages)
            return [p * (100.0 / total) for p in percentages]
    
    def _generate_corporate_documents(self):
        """Generate corporate documents"""
        document_types = [
            "ARTICLES_OF_INCORPORATION",
            "BYLAWS",
            "CERTIFICATE_OF_GOOD_STANDING",
            "BOARD_RESOLUTION",
            "SHAREHOLDERS_REGISTER",
            "BENEFICIAL_OWNERSHIP_REGISTER",
            "UBO_DECLARATION"
        ]
        
        for entity in list(self.structure.entities.values()):
            num_docs = random.randint(3, 7)
            selected_docs = random.sample(document_types, min(num_docs, len(document_types)))
            
            for doc_type in selected_docs:
                doc = CorporateDocument(
                    entity_id=entity.entity_id,
                    document_type=doc_type,
                    jurisdiction=entity.jurisdiction,
                    issue_date=entity.registration_date,
                    effective_date=entity.registration_date,
                    approval_status=random.choice(['DRAFT', 'APPROVED', 'EXECUTED']),
                    compliance_verified=random.random() > 0.2,
                    signatory_persons=[d.person_id for d in entity.get_active_directors()][:2]
                )
                self.structure.add_document(doc)


# ==================== EXPORTERS ====================

class RegistryExporter:
    """Export registry in various formats"""
    
    @staticmethod
    def export_to_json(structure: CorporateStructureGraph, filename: str = 'corporate_registry.json') -> str:
        """Export to JSON"""
        export_data = {
            "export_date": datetime.now().isoformat(),
            "summary": {
                "total_entities": len(structure.entities),
                "total_persons": len(structure.persons),
                "total_documents": len(structure.documents),
                "total_control_chains": len(structure.control_chains)
            },
            "jurisdictions": list(set(e.jurisdiction for e in structure.entities.values())),
            "entities": [entity.to_dict() for entity in structure.entities.values()],
            "persons": [person.to_dict() for person in structure.persons.values()],
            "control_chains": [chain.to_dict() for chain in structure.control_chains.values()],
            "documents": [doc.to_dict() for doc in structure.documents.values()]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return filename
    
    @staticmethod
    def export_to_csv(structure: CorporateStructureGraph, prefix: str = 'registry') -> List[str]:
        """Export to CSV files"""
        files = []
        
        # Entities
        with open(f'{prefix}_entities.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'entity_id', 'legal_name', 'entity_type', 'jurisdiction',
                'registration_number', 'tax_id', 'kyc_status', 'active_status', 'parent_entity_id'
            ])
            writer.writeheader()
            for entity in structure.entities.values():
                writer.writerow({
                    'entity_id': entity.entity_id,
                    'legal_name': entity.legal_name,
                    'entity_type': entity.entity_type,
                    'jurisdiction': entity.jurisdiction,
                    'registration_number': entity.registration_number,
                    'tax_id': entity.tax_id,
                    'kyc_status': entity.kyc_status,
                    'active_status': entity.active_status,
                    'parent_entity_id': entity.parent_entity_id or ''
                })
        files.append(f'{prefix}_entities.csv')
        
        # Persons
        with open(f'{prefix}_persons.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'person_id', 'full_name', 'nationality', 'kyc_status', 'pep_status', 'email', 'passport_number'
            ])
            writer.writeheader()
            for person in structure.persons.values():
                writer.writerow({
                    'person_id': person.person_id,
                    'full_name': person.get_full_name(),
                    'nationality': person.nationality,
                    'kyc_status': person.kyc_status,
                    'pep_status': person.pep_status,
                    'email': person.email or '',
                    'passport_number': person.passport_number or ''
                })
        files.append(f'{prefix}_persons.csv')
        
        # Shareholders
        with open(f'{prefix}_shareholders.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'entity_id', 'shareholder_id', 'person_id', 'entity_owner_id',
                'percentage_ownership', 'share_class', 'is_beneficial_owner'
            ])
            writer.writeheader()
            for entity in structure.entities.values():
                for shareholder in entity.shareholders:
                    writer.writerow({
                        'entity_id': entity.entity_id,
                        'shareholder_id': shareholder.shareholder_id,
                        'person_id': shareholder.person_id or '',
                        'entity_owner_id': shareholder.entity_id or '',
                        'percentage_ownership': shareholder.percentage_ownership,
                        'share_class': shareholder.share_class,
                        'is_beneficial_owner': shareholder.is_beneficial_owner
                    })
        files.append(f'{prefix}_shareholders.csv')
        
        # Directors
        with open(f'{prefix}_directors.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'entity_id', 'director_id', 'person_id', 'title', 'is_active', 'signature_authority'
            ])
            writer.writeheader()
            for entity in structure.entities.values():
                for director in entity.directors:
                    writer.writerow({
                        'entity_id': entity.entity_id,
                        'director_id': director.director_id,
                        'person_id': director.person_id,
                        'title': director.title,
                        'is_active': director.is_active,
                        'signature_authority': director.signature_authority
                    })
        files.append(f'{prefix}_directors.csv')
        
        # Control Chains
        with open(f'{prefix}_control_chains.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'chain_id', 'from_entity_id', 'to_entity_id', 'depth', 'percentage_ownership', 'control_type'
            ])
            writer.writeheader()
            for chain in structure.control_chains.values():
                writer.writerow({
                    'chain_id': chain.chain_id,
                    'from_entity_id': chain.from_entity_id,
                    'to_entity_id': chain.to_entity_id,
                    'depth': chain.get_depth(),
                    'percentage_ownership': chain.percentage_ownership,
                    'control_type': chain.control_type
                })
        files.append(f'{prefix}_control_chains.csv')
        
        return files
    
    @staticmethod
    def generate_compliance_report(structure: CorporateStructureGraph) -> str:
        """Generate compliance report"""
        report = []
        report.append("=" * 100)
        report.append("CORPORATE REGISTRY - COMPLIANCE & STRUCTURE REPORT")
        report.append("=" * 100)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 100)
        report.append(f"Total Entities: {len(structure.entities)}")
        report.append(f"Total Persons: {len(structure.persons)}")
        report.append(f"Total Documents: {len(structure.documents)}")
        report.append(f"Total Control Chains: {len(structure.control_chains)}")
        
        # Jurisdictions
        report.append("\n\nJURISDICTIONAL DISTRIBUTION")
        report.append("-" * 100)
        jurisdiction_summary = structure.get_multi_jurisdiction_summary()
        for juris in sorted(jurisdiction_summary.keys()):
            data = jurisdiction_summary[juris]
            report.append(f"\n{juris}:")
            report.append(f"  Entities: {data['entity_count']}")
            report.append(f"  KYC Verified: {data['kyc_verified']}")
            report.append(f"  KYC Pending: {data['kyc_pending']}")
            report.append(f"  Total Subsidiaries: {data['total_subsidiaries']}")
        
        # KYC Status
        report.append("\n\nKYC COMPLIANCE STATUS")
        report.append("-" * 100)
        kyc_breakdown = {'VERIFIED': 0, 'PENDING': 0, 'REJECTED': 0}
        for entity in structure.entities.values():
            status = entity.kyc_status
            kyc_breakdown[status] = kyc_breakdown.get(status, 0) + 1
        
        for status, count in sorted(kyc_breakdown.items()):
            percentage = (count / len(structure.entities) * 100) if structure.entities else 0
            report.append(f"{status}: {count} ({percentage:.1f}%)")
        
        # PEP & Sanctions
        report.append("\n\nPEP & SANCTIONS SCREENING")
        report.append("-" * 100)
        pep_count = sum(1 for p in structure.persons.values() if p.pep_status)
        sanctions_count = sum(1 for p in structure.persons.values() if p.sanctions_status)
        
        report.append(f"Persons with PEP Status: {pep_count}")
        if pep_count > 0:
            for person in [p for p in structure.persons.values() if p.pep_status][:5]:
                report.append(f"  • {person.get_full_name()} ({person.nationality})")
        
        report.append(f"\nPersons with Sanctions: {sanctions_count}")
        
        # Control Chain Integrity
        report.append("\n\nCONTROL CHAIN ANALYSIS")
        report.append("-" * 100)
        issues = structure.verify_control_chain_integrity()
        if issues:
            report.append(f"Issues Found: {len(issues)}")
            for issue in issues[:10]:
                report.append(f"  ⚠ {issue}")
        else:
            report.append("✓ All control chains verified - No circular references detected")
        
        # Ownership Structure
        report.append("\n\nOWNERSHIP STRUCTURE OVERVIEW")
        report.append("-" * 100)
        holding_companies = [e for e in structure.entities.values() if e.entity_type == "HOLDING_COMPANY"]
        report.append(f"Holding Companies: {len(holding_companies)}")
        for holding in holding_companies[:3]:
            report.append(f"\n  {holding.legal_name}")
            report.append(f"    Jurisdiction: {holding.jurisdiction}")
            report.append(f"    Direct Shareholders: {len(holding.shareholders)}")
            report.append(f"    Subsidiaries: {len(holding.subsidiary_entity_ids)}")
            report.append(f"    KYC Status: {holding.kyc_status}")
        
        # Document Status
        report.append("\n\nCORPORATE DOCUMENTS STATUS")
        report.append("-" * 100)
        doc_statuses = {}
        for doc in structure.documents.values():
            status = doc.approval_status
            doc_statuses[status] = doc_statuses.get(status, 0) + 1
        
        for status, count in sorted(doc_statuses.items()):
            report.append(f"{status}: {count}")
        
        report.append("\n" + "=" * 100 + "\n")
        
        return "\n".join(report)


# ==================== MAIN EXECUTION ====================

def main():
    """Main execution"""
    print("\n" + "=" * 100)
    print("COMPREHENSIVE CORPORATE REGISTRY GENERATOR")
    print("Multi-Jurisdictional Structure with Indirect Control")
    print("=" * 100 + "\n")
    
    # Generate registry
    print("→ Generating multi-level holding company structure...")
    generator = CorporateRegistryGenerator()
    structure = generator.generate_multi_level_holding_structure(
        num_holding_companies=2,
        num_subsidiaries_per_holding=3,
        num_sub_subsidiaries=2
    )
    
    print(f"  ✓ Generated {len(structure.entities)} entities")
    print(f"  ✓ Generated {len(structure.persons)} persons")
    print(f"  ✓ Generated {len(structure.documents)} documents")
    print(f"  ✓ Generated {len(structure.control_chains)} control chains\n")
    
    # Export to JSON
    print("→ Exporting to JSON...")
    json_file = RegistryExporter.export_to_json(structure, 'corporate_registry.json')
    print(f"  ✓ Saved to {json_file}\n")
    
    # Export to CSV
    print("→ Exporting to CSV files...")
    csv_files = RegistryExporter.export_to_csv(structure, 'corporate_registry')
    for csv_file in csv_files:
        print(f"  ✓ Saved to {csv_file}")
    print()
    
    # Generate compliance report
    print("→ Generating compliance report...")
    report = RegistryExporter.generate_compliance_report(structure)
    print(report)
    
    with open('corporate_registry_compliance_report.txt', 'w') as f:
        f.write(report)
    print("  ✓ Report saved to corporate_registry_compliance_report.txt\n")
    
    # Show sample hierarchy
    print("→ SAMPLE OWNERSHIP HIERARCHY")
    print("-" * 100)
    
    operating_companies = [e for e in structure.entities.values() 
                          if e.entity_type in ["LLC", "CORPORATION", "SUBSIDIARY"]]
    if operating_companies:
        sample = operating_companies[0]
        hierarchy = structure.get_ownership_hierarchy(sample.entity_id)
        
        print(f"\nEntity: {hierarchy['entity']['legal_name']}")
        print(f"Type: {hierarchy['entity']['entity_type']}")
        print(f"Jurisdiction: {hierarchy['entity']['jurisdiction']}")
        print(f"Registration: {hierarchy['entity']['registration_number']}")
        print(f"Tax ID: {hierarchy['entity']['tax_id']}")
        print(f"KYC Status: {hierarchy['entity']['kyc_status']}")
        
        if hierarchy['shareholders']:
            print(f"\nDirect Shareholders ({len(hierarchy['shareholders'])}):")
            for sh in hierarchy['shareholders'][:5]:
                print(f"  • {sh.get('name', 'Unknown')} ({sh['type']}): {sh['percentage']:.1f}%")
        
        if hierarchy['directors']:
            print(f"\nDirectors ({len(hierarchy['directors'])}):")
            for dir in hierarchy['directors'][:3]:
                status = "Active" if dir['active'] else "Inactive"
                print(f"  • {dir['name']} - {dir['title']} ({status})")
        
        if hierarchy['control_chains']:
            print(f"\nControl Chains ({len(hierarchy['control_chains'])}):")
            for cc in hierarchy['control_chains'][:3]:
                print(f"  • Depth: {cc['depth']} levels, Ownership: {cc['percentage']:.1f}%")
    
    print("\n" + "=" * 100)
    print("Corporate registry generation complete!")
    print("=" * 100 + "\n")
    
    # Print file locations
    print("Generated Files:")
    print(f"  1. corporate_registry.json")
    print(f"  2. corporate_registry_entities.csv")
    print(f"  3. corporate_registry_persons.csv")
    print(f"  4. corporate_registry_shareholders.csv")
    print(f"  5. corporate_registry_directors.csv")
    print(f"  6. corporate_registry_control_chains.csv")
    print(f"  7. corporate_registry_compliance_report.txt\n")


if __name__ == "__main__":
    main()
