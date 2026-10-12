"""
Multi-Jurisdictional Corporate Documents Framework
Manages complex entity structures with multiple jurisdictions and indirect control
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime
from abc import ABC, abstractmethod
import json
import uuid


class JurisdictionType(Enum):
    """Supported jurisdictions"""
    US_FEDERAL = "US_FEDERAL"
    US_STATE = "US_STATE"
    UK = "UK"
    CAYMAN_ISLANDS = "CAYMAN_ISLANDS"
    LUXEMBOURG = "LUXEMBOURG"
    SINGAPORE = "SINGAPORE"
    UAE = "UAE"
    HONG_KONG = "HONG_KONG"
    BVI = "BVI"  # British Virgin Islands
    MALTA = "MALTA"


class EntityType(Enum):
    """Types of corporate entities"""
    CORPORATION = "CORPORATION"
    LLC = "LLC"
    PARTNERSHIP = "PARTNERSHIP"
    TRUST = "TRUST"
    FOUNDATION = "FOUNDATION"
    COOPERATIVE = "COOPERATIVE"
    JOINT_VENTURE = "JOINT_VENTURE"
    HOLDING_COMPANY = "HOLDING_COMPANY"
    OFFSHORE_COMPANY = "OFFSHORE_COMPANY"
    BRANCH = "BRANCH"
    SUBSIDIARY = "SUBSIDIARY"


class OwnershipType(Enum):
    """Types of ownership/control"""
    DIRECT = "DIRECT"
    INDIRECT = "INDIRECT"
    BENEFICIAL = "BENEFICIAL"
    NOMINEE = "NOMINEE"
    TRUSTEE = "TRUSTEE"
    POWER_OF_ATTORNEY = "POWER_OF_ATTORNEY"


class DocumentType(Enum):
    """Corporate document types"""
    ARTICLES_OF_INCORPORATION = "ARTICLES_OF_INCORPORATION"
    BYLAWS = "BYLAWS"
    OPERATING_AGREEMENT = "OPERATING_AGREEMENT"
    PARTNERSHIP_AGREEMENT = "PARTNERSHIP_AGREEMENT"
    SHAREHOLDERS_AGREEMENT = "SHAREHOLDERS_AGREEMENT"
    CERTIFICATE_OF_GOOD_STANDING = "CERTIFICATE_OF_GOOD_STANDING"
    BOARD_RESOLUTION = "BOARD_RESOLUTION"
    MINUTES_OF_MEETING = "MINUTES_OF_MEETING"
    CERTIFICATE_OF_INCORPORATION = "CERTIFICATE_OF_INCORPORATION"
    POWER_OF_ATTORNEY = "POWER_OF_ATTORNEY"
    DIRECTORS_REGISTER = "DIRECTORS_REGISTER"
    SHAREHOLDERS_REGISTER = "SHAREHOLDERS_REGISTER"
    BENEFICIAL_OWNERSHIP_REGISTER = "BENEFICIAL_OWNERSHIP_REGISTER"
    TRUST_DEED = "TRUST_DEED"
    FOUNDATION_CHARTER = "FOUNDATION_CHARTER"
    CORPORATE_GOVERNANCE_MANUAL = "CORPORATE_GOVERNANCE_MANUAL"
    COMPLIANCE_CERTIFICATE = "COMPLIANCE_CERTIFICATE"
    UBO_DECLARATION = "UBO_DECLARATION"  # Ultimate Beneficial Owner


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
    kyc_status: str = "PENDING"  # PENDING, VERIFIED, REJECTED
    kyc_date: Optional[str] = None
    pep_status: bool = False  # Politically Exposed Person
    sanctions_status: bool = False
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


@dataclass
class ControlChain:
    """Represents indirect control through intermediary entities"""
    chain_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_entity_id: str = ""
    to_entity_id: str = ""
    path: List[str] = field(default_factory=list)  # Ordered list of entity IDs
    percentage_ownership: float = 0.0
    control_type: OwnershipType = OwnershipType.INDIRECT
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_depth(self) -> int:
        """Returns the number of intermediary entities"""
        return len(self.path) - 2 if len(self.path) > 1 else 0
    
    def is_circular(self) -> bool:
        """Check if control chain creates a circular reference"""
        return len(self.path) != len(set(self.path))


@dataclass
class Shareholder:
    """Shareholder record with ownership details"""
    shareholder_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: Optional[str] = None  # If shareholder is an entity
    person_id: Optional[str] = None  # If shareholder is an individual
    shares_issued: int = 0
    share_class: str = "COMMON"  # COMMON, PREFERRED, etc.
    percentage_ownership: float = 0.0
    voting_rights: float = 0.0
    acquisition_date: str = ""
    is_beneficial_owner: bool = False
    
    def is_individual(self) -> bool:
        return self.person_id is not None and self.entity_id is None
    
    def is_entity(self) -> bool:
        return self.entity_id is not None and self.person_id is None


@dataclass
class Director:
    """Director/Officer record"""
    director_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    person_id: str = ""
    title: str = ""  # CEO, CFO, Director, etc.
    appointment_date: str = ""
    resignation_date: Optional[str] = None
    is_active: bool = True
    responsibilities: List[str] = field(default_factory=list)
    signature_authority: bool = False
    compensation: Optional[float] = None
    
    def is_current(self) -> bool:
        return self.is_active and self.resignation_date is None


@dataclass
class CorporateDocument:
    """Represents a corporate document"""
    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str = ""
    document_type: DocumentType = DocumentType.ARTICLES_OF_INCORPORATION
    jurisdiction: JurisdictionType = JurisdictionType.US_FEDERAL
    issue_date: str = ""
    effective_date: str = ""
    expiry_date: Optional[str] = None
    file_path: str = ""
    document_hash: Optional[str] = None  # SHA-256 hash for integrity
    signatory_persons: List[str] = field(default_factory=list)  # Person IDs
    approval_status: str = "DRAFT"  # DRAFT, APPROVED, EXECUTED, ARCHIVED
    compliance_verified: bool = False
    metadata: Dict = field(default_factory=dict)
    content_summary: str = ""


@dataclass
class CorporateEntity:
    """Represents a corporate entity in the structure"""
    entity_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    legal_name: str = ""
    entity_type: EntityType = EntityType.CORPORATION
    jurisdiction: JurisdictionType = JurisdictionType.US_FEDERAL
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
    authorized_signatories: List[str] = field(default_factory=list)  # Person IDs
    
    # Control information
    control_chains: List[ControlChain] = field(default_factory=list)
    beneficial_owners: List[str] = field(default_factory=list)  # Person IDs
    
    # Documents
    corporate_documents: List[CorporateDocument] = field(default_factory=list)
    
    # Compliance
    kyc_status: str = "PENDING"
    kyc_completion_date: Optional[str] = None
    last_audit_date: Optional[str] = None
    compliance_notes: str = ""
    
    def add_shareholder(self, shareholder: Shareholder):
        """Add shareholder to entity"""
        self.shareholders.append(shareholder)
    
    def add_director(self, director: Director):
        """Add director to entity"""
        self.directors.append(director)
    
    def get_active_directors(self) -> List[Director]:
        """Get currently active directors"""
        return [d for d in self.directors if d.is_current()]
    
    def get_ultimate_beneficial_owners(self) -> List[str]:
        """Calculate ultimate beneficial owners through control chains"""
        ubos = set()
        for bo in self.beneficial_owners:
            ubos.add(bo)
        
        # Trace through control chains
        for chain in self.control_chains:
            if chain.to_entity_id == self.entity_id:
                ubos.add(chain.from_entity_id)
        
        return list(ubos)
    
    def get_total_capitalization(self) -> float:
        """Calculate total capitalization from shareholders"""
        total = sum(sh.percentage_ownership for sh in self.shareholders)
        return total
    
    def add_control_chain(self, chain: ControlChain):
        """Add control chain"""
        if not chain.is_circular():
            self.control_chains.append(chain)
    
    def to_dict(self) -> Dict:
        """Convert entity to dictionary"""
        return {
            "entity_id": self.entity_id,
            "legal_name": self.legal_name,
            "entity_type": self.entity_type.value,
            "jurisdiction": self.jurisdiction.value,
            "registration_number": self.registration_number,
            "tax_id": self.tax_id,
            "active_status": self.active_status,
            "shareholders_count": len(self.shareholders),
            "directors_count": len(self.directors),
            "subsidiary_count": len(self.subsidiary_entity_ids),
            "kyc_status": self.kyc_status
        }


class CorporateStructureGraph:
    """Manages complex multi-entity corporate structure"""
    
    def __init__(self):
        self.entities: Dict[str, CorporateEntity] = {}
        self.persons: Dict[str, Person] = {}
        self.documents: Dict[str, CorporateDocument] = {}
        self.control_chains: Dict[str, ControlChain] = {}
    
    def add_entity(self, entity: CorporateEntity):
        """Add entity to structure"""
        self.entities[entity.entity_id] = entity
    
    def add_person(self, person: Person):
        """Add person to structure"""
        self.persons[person.person_id] = person
    
    def add_document(self, document: CorporateDocument):
        """Add document to structure"""
        self.documents[document.document_id] = document
        if document.entity_id in self.entities:
            self.entities[document.entity_id].corporate_documents.append(document)
    
    def add_control_chain(self, chain: ControlChain):
        """Add control chain"""
        self.control_chains[chain.chain_id] = chain
        if chain.to_entity_id in self.entities:
            self.entities[chain.to_entity_id].add_control_chain(chain)
    
    def get_ownership_hierarchy(self, entity_id: str, max_depth: int = 10) -> Dict:
        """Get full ownership hierarchy for an entity"""
        if entity_id not in self.entities:
            return {}
        
        entity = self.entities[entity_id]
        hierarchy = {
            "entity": entity.to_dict(),
            "shareholders": [],
            "indirect_owners": [],
            "ultimate_beneficial_owners": []
        }
        
        # Direct shareholders
        for shareholder in entity.shareholders:
            sh_info = {
                "shareholder_id": shareholder.shareholder_id,
                "percentage": shareholder.percentage_ownership,
                "ownership_type": shareholder.share_class
            }
            if shareholder.person_id and shareholder.person_id in self.persons:
                person = self.persons[shareholder.person_id]
                sh_info["name"] = person.get_full_name()
                sh_info["type"] = "INDIVIDUAL"
            elif shareholder.entity_id and shareholder.entity_id in self.entities:
                sh_info["name"] = self.entities[shareholder.entity_id].legal_name
                sh_info["type"] = "ENTITY"
            
            hierarchy["shareholders"].append(sh_info)
        
        # Indirect ownership through control chains
        for chain in entity.control_chains:
            if chain.to_entity_id == entity_id:
                chain_info = {
                    "chain_id": chain.chain_id,
                    "percentage": chain.percentage_ownership,
                    "depth": chain.get_depth(),
                    "path": [self.entities[eid].legal_name if eid in self.entities else eid 
                            for eid in chain.path]
                }
                hierarchy["indirect_owners"].append(chain_info)
        
        # Ultimate beneficial owners
        for ubo_id in entity.get_ultimate_beneficial_owners():
            if ubo_id in self.persons:
                ubo_info = {
                    "id": ubo_id,
                    "name": self.persons[ubo_id].get_full_name(),
                    "type": "INDIVIDUAL",
                    "kyc_status": self.persons[ubo_id].kyc_status
                }
                hierarchy["ultimate_beneficial_owners"].append(ubo_info)
            elif ubo_id in self.entities:
                ubo_info = {
                    "id": ubo_id,
                    "name": self.entities[ubo_id].legal_name,
                    "type": "ENTITY",
                    "kyc_status": self.entities[ubo_id].kyc_status
                }
                hierarchy["ultimate_beneficial_owners"].append(ubo_info)
        
        return hierarchy
    
    def get_all_connected_entities(self, entity_id: str) -> Set[str]:
        """Get all entities connected through ownership/control"""
        connected = {entity_id}
        to_process = [entity_id]
        
        while to_process:
            current_id = to_process.pop(0)
            if current_id not in self.entities:
                continue
            
            entity = self.entities[current_id]
            
            # Add subsidiaries
            for sub_id in entity.subsidiary_entity_ids:
                if sub_id not in connected:
                    connected.add(sub_id)
                    to_process.append(sub_id)
            
            # Add parent
            if entity.parent_entity_id and entity.parent_entity_id not in connected:
                connected.add(entity.parent_entity_id)
                to_process.append(entity.parent_entity_id)
            
            # Add entities through control chains
            for chain in entity.control_chains:
                if chain.from_entity_id not in connected:
                    connected.add(chain.from_entity_id)
                    to_process.append(chain.from_entity_id)
        
        return connected
    
    def verify_control_chain_integrity(self) -> List[str]:
        """Verify all control chains for issues"""
        issues = []
        
        for chain_id, chain in self.control_chains.items():
            # Check for circular references
            if chain.is_circular():
                issues.append(f"Circular control chain detected: {chain_id}")
            
            # Check if all entities in path exist
            for entity_id in chain.path:
                if entity_id not in self.entities:
                    issues.append(f"Entity {entity_id} not found in chain {chain_id}")
            
            # Verify ownership percentages
            if chain.percentage_ownership < 0 or chain.percentage_ownership > 100:
                issues.append(f"Invalid ownership percentage in chain {chain_id}")
        
        return issues
    
    def get_compliance_summary(self, entity_id: str) -> Dict:
        """Get KYC/compliance summary for entity and all stakeholders"""
        if entity_id not in self.entities:
            return {}
        
        entity = self.entities[entity_id]
        summary = {
            "entity_id": entity_id,
            "entity_kyc_status": entity.kyc_status,
            "directors_compliance": [],
            "shareholders_compliance": [],
            "beneficial_owners_compliance": [],
            "documents_status": [],
            "overall_compliance": "COMPLIANT"
        }
        
        # Check directors
        for director in entity.get_active_directors():
            if director.person_id in self.persons:
                person = self.persons[director.person_id]
                summary["directors_compliance"].append({
                    "name": person.get_full_name(),
                    "kyc_status": person.kyc_status,
                    "pep_status": person.pep_status,
                    "sanctions_status": person.sanctions_status
                })
        
        # Check shareholders
        for shareholder in entity.shareholders:
            if shareholder.person_id and shareholder.person_id in self.persons:
                person = self.persons[shareholder.person_id]
                summary["shareholders_compliance"].append({
                    "name": person.get_full_name(),
                    "kyc_status": person.kyc_status,
                    "percentage": shareholder.percentage_ownership
                })
        
        # Check beneficial owners
        for ubo_id in entity.beneficial_owners:
            if ubo_id in self.persons:
                person = self.persons[ubo_id]
                summary["beneficial_owners_compliance"].append({
                    "name": person.get_full_name(),
                    "kyc_status": person.kyc_status
                })
        
        # Check documents
        for doc in entity.corporate_documents:
            summary["documents_status"].append({
                "type": doc.document_type.value,
                "status": doc.approval_status,
                "compliance_verified": doc.compliance_verified
            })
        
        # Determine overall compliance
        if entity.kyc_status != "VERIFIED":
            summary["overall_compliance"] = "NON_COMPLIANT"
        
        return summary
    
    def export_structure_json(self) -> str:
        """Export entire structure as JSON"""
        export_data = {
            "entities": [entity.to_dict() for entity in self.entities.values()],
            "total_entities": len(self.entities),
            "total_persons": len(self.persons),
            "total_documents": len(self.documents),
            "total_control_chains": len(self.control_chains),
            "export_date": datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2)
    
    def get_multi_jurisdiction_summary(self) -> Dict:
        """Summarize structure across jurisdictions"""
        jurisdiction_summary = {}
        
        for entity in self.entities.values():
            juris = entity.jurisdiction.value
            if juris not in jurisdiction_summary:
                jurisdiction_summary[juris] = {
                    "entity_count": 0,
                    "entities": [],
                    "total_subsidiaries": 0,
                    "kyc_status": {}
                }
            
            jurisdiction_summary[juris]["entity_count"] += 1
            jurisdiction_summary[juris]["entities"].append(entity.legal_name)
            jurisdiction_summary[juris]["total_subsidiaries"] += len(entity.subsidiary_entity_ids)
            
            status = entity.kyc_status
            if status not in jurisdiction_summary[juris]["kyc_status"]:
                jurisdiction_summary[juris]["kyc_status"][status] = 0
            jurisdiction_summary[juris]["kyc_status"][status] += 1
        
        return jurisdiction_summary


# Example usage demonstration
if __name__ == "__main__":
    # Create the corporate structure graph
    structure = CorporateStructureGraph()
    
    # Create persons (beneficial owners)
    john_doe = Person(
        first_name="John",
        last_name="Doe",
        nationality="US",
        residential_address="123 Main St, New York, NY",
        kyc_status="VERIFIED"
    )
    jane_smith = Person(
        first_name="Jane",
        last_name="Smith",
        nationality="UK",
        residential_address="456 Oxford St, London, UK",
        kyc_status="VERIFIED"
    )
    
    structure.add_person(john_doe)
    structure.add_person(jane_smith)
    
    # Create holding company (Cayman Islands)
    holding_co = CorporateEntity(
        legal_name="Global Holdings Ltd",
        entity_type=EntityType.HOLDING_COMPANY,
        jurisdiction=JurisdictionType.CAYMAN_ISLANDS,
        registration_number="C12345",
        registration_date="2023-01-15",
        tax_id="TAX001",
        business_address="Cayman Islands",
        kyc_status="VERIFIED"
    )
    structure.add_entity(holding_co)
    
    # Add shareholders to holding company
    shareholder1 = Shareholder(
        person_id=john_doe.person_id,
        shares_issued=500,
        percentage_ownership=50.0,
        is_beneficial_owner=True,
        acquisition_date="2023-01-15"
    )
    shareholder2 = Shareholder(
        person_id=jane_smith.person_id,
        shares_issued=500,
        percentage_ownership=50.0,
        is_beneficial_owner=True,
        acquisition_date="2023-01-15"
    )
    holding_co.add_shareholder(shareholder1)
    holding_co.add_shareholder(shareholder2)
    holding_co.beneficial_owners = [john_doe.person_id, jane_smith.person_id]
    
    # Create US Operating Company
    us_operating = CorporateEntity(
        legal_name="Global Operations LLC",
        entity_type=EntityType.LLC,
        jurisdiction=JurisdictionType.US_STATE,
        state_province="Delaware",
        registration_number="LLC001",
        registration_date="2023-02-01",
        tax_id="TAX002",
        business_address="100 Delaware Ave, Wilmington, DE",
        parent_entity_id=holding_co.entity_id,
        kyc_status="VERIFIED"
    )
    holding_co.subsidiary_entity_ids.append(us_operating.entity_id)
    structure.add_entity(us_operating)
    
    # Add holding company as shareholder of operating company
    shareholder3 = Shareholder(
        entity_id=holding_co.entity_id,
        shares_issued=100,
        percentage_ownership=100.0,
        is_beneficial_owner=False,
        acquisition_date="2023-02-01"
    )
    us_operating.add_shareholder(shareholder3)
    
    # Create control chain (indirect ownership)
    control_chain = ControlChain(
        from_entity_id=holding_co.entity_id,
        to_entity_id=us_operating.entity_id,
        path=[holding_co.entity_id, us_operating.entity_id],
        percentage_ownership=100.0,
        control_type=OwnershipType.INDIRECT
    )
    structure.add_control_chain(control_chain)
    
    # Create UK Entity
    uk_entity = CorporateEntity(
        legal_name="Global UK Ltd",
        entity_type=EntityType.CORPORATION,
        jurisdiction=JurisdictionType.UK,
        registration_number="UK12345",
        registration_date="2023-03-01",
        tax_id="TAX003",
        business_address="789 London Way, London, UK",
        kyc_status="VERIFIED"
    )
    structure.add_entity(uk_entity)
    
    # Add holding company as shareholder
    shareholder4 = Shareholder(
        entity_id=holding_co.entity_id,
        shares_issued=1000,
        percentage_ownership=100.0,
        is_beneficial_owner=False,
        acquisition_date="2023-03-01"
    )
    uk_entity.add_shareholder(shareholder4)
    
    # Create Singapore subsidiary
    sg_subsidiary = CorporateEntity(
        legal_name="Global Asia Pte Ltd",
        entity_type=EntityType.SUBSIDIARY,
        jurisdiction=JurisdictionType.SINGAPORE,
        registration_number="SG567890",
        registration_date="2023-04-01",
        tax_id="TAX004",
        business_address="123 Marina Bay, Singapore",
        parent_entity_id=us_operating.entity_id,
        kyc_status="VERIFIED"
    )
    us_operating.subsidiary_entity_ids.append(sg_subsidiary.entity_id)
    structure.add_entity(sg_subsidiary)
    
    # Add directors to operating company
    director1 = Director(
        person_id=john_doe.person_id,
        title="CEO",
        appointment_date="2023-02-01",
        is_active=True,
        signature_authority=True
    )
    us_operating.add_director(director1)
    
    director2 = Director(
        person_id=jane_smith.person_id,
        title="CFO",
        appointment_date="2023-02-01",
        is_active=True,
        signature_authority=True
    )
    us_operating.add_director(director2)
    
    # Create corporate documents
    articles = CorporateDocument(
        entity_id=us_operating.entity_id,
        document_type=DocumentType.ARTICLES_OF_INCORPORATION,
        jurisdiction=JurisdictionType.US_STATE,
        issue_date="2023-02-01",
        effective_date="2023-02-01",
        approval_status="EXECUTED",
        compliance_verified=True,
        signatory_persons=[john_doe.person_id, jane_smith.person_id]
    )
    structure.add_document(articles)
    
    # Print structure summary
    print("=== CORPORATE STRUCTURE SUMMARY ===\n")
    print(structure.get_multi_jurisdiction_summary())
    print("\n=== OWNERSHIP HIERARCHY ===\n")
    print(json.dumps(structure.get_ownership_hierarchy(us_operating.entity_id), indent=2))
    print("\n=== COMPLIANCE SUMMARY ===\n")
    print(json.dumps(structure.get_compliance_summary(us_operating.entity_id), indent=2))
    print("\n=== CONTROL CHAIN VERIFICATION ===\n")
    print(structure.verify_control_chain_integrity())
