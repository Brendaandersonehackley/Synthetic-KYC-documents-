"""
Full Corporate Registry Generator with Realistic Sample Data
Generates complex multi-jurisdictional corporate structures with synthetic but realistic data
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from corporate_documents_framework import (
    CorporateStructureGraph,
    CorporateEntity,
    Person,
    Shareholder,
    Director,
    CorporateDocument,
    ControlChain,
    JurisdictionType,
    EntityType,
    DocumentType,
    OwnershipType
)


class RealisticDataGenerator:
    """Generates realistic synthetic data for corporate structures"""
    
    # Realistic first and last names by nationality
    FIRST_NAMES = {
        'US': ['John', 'Sarah', 'Michael', 'Jennifer', 'Robert', 'Emily', 'James', 'Mary'],
        'UK': ['William', 'Lucy', 'Oliver', 'Amelia', 'George', 'Sophie', 'Harry', 'Olivia'],
        'Singapore': ['Wei', 'Li', 'Chen', 'Lim', 'Tan', 'Wong', 'Ng', 'Koh'],
        'Hong Kong': ['Zhang', 'Liu', 'Wang', 'Li', 'Yang', 'Huang', 'Zhao', 'Wu'],
        'UAE': ['Mohammed', 'Ahmed', 'Fatima', 'Aisha', 'Hassan', 'Layla', 'Omar', 'Noor'],
        'Luxembourg': ['Jean', 'Marie', 'Pierre', 'Anne', 'Jacques', 'Sophie', 'Michel', 'Isabelle'],
        'Malta': ['Angelo', 'Maria', 'Joseph', 'Francesca', 'Paul', 'Theresa', 'Antonio', 'Camilla'],
        'Cayman Islands': ['James', 'Patricia', 'Michael', 'Jennifer', 'David', 'Margaret', 'Richard', 'Susan'],
        'BVI': ['Thomas', 'Barbara', 'Charles', 'Karen', 'Daniel', 'Nancy', 'Matthew', 'Lisa'],
    }
    
    LAST_NAMES = {
        'US': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'],
        'UK': ['Thompson', 'Bennett', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Peterson'],
        'Singapore': ['Ong', 'Lee', 'Chua', 'Lau', 'Quek', 'Yap', 'Soh', 'Pang'],
        'Hong Kong': ['Chan', 'Wong', 'Leung', 'Cheng', 'Tang', 'Kwok', 'Poon', 'Tam'],
        'UAE': ['Al Maktoum', 'Al Nahyan', 'Al Qassimi', 'Al Mansoori', 'Al Mutawa', 'Al Suwaidi'],
        'Luxembourg': ['Muller', 'Schmidt', 'Wagner', 'Schneider', 'Fischer', 'Weber', 'Meyer'],
        'Malta': ['Vella', 'Grech', 'Schembri', 'Azzopardi', 'Micallef', 'Camilleri', 'Galea'],
        'Cayman Islands': ['Taylor', 'Anderson', 'Thomas', 'Moore', 'Jackson', 'Martin', 'Perry'],
        'BVI': ['Harper', 'Fuller', 'Austin', 'Mendez', 'Graham', 'Sullivan', 'Wallace'],
    }
    
    # Company name patterns
    COMPANY_PREFIXES = [
        'Global', 'International', 'Premier', 'Alliance', 'Capital', 'Equity', 
        'Strategic', 'Vertex', 'Apex', 'Zenith', 'Meridian', 'Nexus', 'Quantum',
        'Trinity', 'Vanguard', 'Paramount', 'Imperial', 'Royal', 'Elite', 'Exclusive'
    ]
    
    COMPANY_SUFFIXES = [
        'Holdings', 'Investment', 'Partners', 'Group', 'Solutions', 'Ventures',
        'Corporation', 'Management', 'Enterprises', 'Finance', 'Capital', 'Assets',
        'Services', 'Advisors', 'Trust', 'Fund'
    ]
    
    COMPANY_SECTORS = [
        'Technology', 'Finance', 'Real Estate', 'Energy', 'Healthcare',
        'Manufacturing', 'Retail', 'Logistics', 'Media', 'Telecommunications'
    ]
    
    TITLES = ['CEO', 'CFO', 'COO', 'CTO', 'President', 'Vice President', 
              'Director', 'Executive Director', 'Chairman', 'Treasurer', 'Secretary']
    
    @staticmethod
    def generate_person(nationality: str = 'US', is_director: bool = False) -> Person:
        """Generate a realistic person"""
        first_names = RealisticDataGenerator.FIRST_NAMES.get(nationality, RealisticDataGenerator.FIRST_NAMES['US'])
        last_names = RealisticDataGenerator.LAST_NAMES.get(nationality, RealisticDataGenerator.LAST_NAMES['US'])
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        middle_name = random.choice(first_names) if random.random() > 0.4 else None
        
        # Generate realistic dates
        birth_year = random.randint(1960, 2000)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        dob = f"{birth_year:04d}-{birth_month:02d}-{birth_day:02d}"
        
        # Realistic addresses
        if nationality == 'US':
            states = ['NY', 'CA', 'TX', 'FL', 'IL', 'PA', 'OH', 'MI', 'DE']
            state = random.choice(states)
            residential = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Park', 'Washington', 'Madison'])} St, {random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])}, {state} {random.randint(10000, 99999)}"
        elif nationality == 'UK':
            residential = f"{random.randint(100, 9999)} {random.choice(['High', 'Bond', 'Oxford', 'Fleet', 'Regent'])} Street, London, {random.choice(['SW1', 'W1', 'EC1', 'N1'])} {random.randint(1, 9)}{random.choice(['A', 'B', 'C', 'D'])}"
        else:
            residential = f"{random.randint(100, 9999)} {random.choice(['Central', 'Main', 'Victoria', 'Marina'])} {random.choice(['Avenue', 'Street', 'Road', 'Boulevard'])}"
        
        person = Person(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            date_of_birth=dob,
            nationality=nationality,
            passport_number=f"{nationality[:2].upper()}{random.randint(10000000, 99999999)}",
            id_number=f"{random.randint(100000000, 999999999)}",
            email=f"{first_name.lower()}.{last_name.lower()}@{random.choice(['corporate.com', 'business.com', 'group.com'])}",
            phone=f"+{random.randint(1, 65)}{random.randint(10000000, 999999999)}",
            residential_address=residential,
            kyc_status=random.choice(['VERIFIED', 'VERIFIED', 'VERIFIED', 'PENDING']),
            pep_status=random.random() < 0.05,  # 5% PEP
            sanctions_status=False
        )
        
        if person.kyc_status == 'VERIFIED':
            person.kyc_date = (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat()
        
        return person
    
    @staticmethod
    def generate_company_name() -> str:
        """Generate a realistic company name"""
        prefix = random.choice(RealisticDataGenerator.COMPANY_PREFIXES)
        sector = random.choice(RealisticDataGenerator.COMPANY_SECTORS)
        suffix = random.choice(RealisticDataGenerator.COMPANY_SUFFIXES)
        return f"{prefix} {sector} {suffix}"
    
    @staticmethod
    def generate_tax_id(jurisdiction: JurisdictionType) -> str:
        """Generate realistic tax ID based on jurisdiction"""
        if jurisdiction == JurisdictionType.US_FEDERAL:
            return f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"
        elif jurisdiction == JurisdictionType.US_STATE:
            return f"EIN{random.randint(10000000, 99999999)}"
        elif jurisdiction == JurisdictionType.UK:
            return f"{random.randint(100000000, 999999999)}"
        elif jurisdiction == JurisdictionType.SINGAPORE:
            return f"{random.randint(100000000, 999999999)}"
        else:
            return f"TAX{random.randint(1000000, 9999999)}"
    
    @staticmethod
    def generate_registration_number(jurisdiction: JurisdictionType) -> str:
        """Generate realistic registration number"""
        if jurisdiction == JurisdictionType.US_STATE:
            return f"{random.randint(1000000, 9999999)}"
        elif jurisdiction == JurisdictionType.UK:
            return f"{random.randint(1000000, 9999999)}"
        elif jurisdiction == JurisdictionType.CAYMAN_ISLANDS:
            return f"C{random.randint(1000000, 9999999)}"
        elif jurisdiction == JurisdictionType.SINGAPORE:
            return f"{random.randint(100000000, 999999999)}"
        elif jurisdiction == JurisdictionType.HONG_KONG:
            return f"{random.randint(1000000, 9999999)}"
        else:
            return f"REG{random.randint(1000000, 9999999)}"
    
    @staticmethod
    def get_jurisdiction_address(jurisdiction: JurisdictionType) -> str:
        """Get realistic address for jurisdiction"""
        addresses = {
            JurisdictionType.US_STATE: f"{random.randint(100, 5000)} Delaware Ave, Wilmington, DE {random.randint(10000, 19999)}",
            JurisdictionType.US_FEDERAL: f"{random.randint(100, 5000)} Main Street, New York, NY {random.randint(10000, 19999)}",
            JurisdictionType.UK: f"{random.randint(100, 5000)} {random.choice(['Canary', 'Broadgate', 'Lombard'])} {random.choice(['Street', 'Place', 'Lane'])}, London EC2",
            JurisdictionType.CAYMAN_ISLANDS: f"{random.randint(100, 5000)} Cayman Business Park, George Town, KY1-1108",
            JurisdictionType.LUXEMBOURG: f"{random.randint(100, 5000)} rue de la Toison d'Or, Luxembourg City L-2113",
            JurisdictionType.SINGAPORE: f"{random.randint(100, 5000)} Marina Bay, Singapore {random.randint(100000, 999999)}",
            JurisdictionType.UAE: f"{random.randint(100, 5000)} Business Bay, Dubai, UAE",
            JurisdictionType.HONG_KONG: f"{random.randint(100, 5000)} Central, Hong Kong",
            JurisdictionType.BVI: f"{random.randint(100, 5000)} Main Street, Road Town, Tortola",
            JurisdictionType.MALTA: f"{random.randint(100, 5000)} Valletta, Malta"
        }
        return addresses.get(jurisdiction, f"{random.randint(100, 5000)} Business Street")


class CorporateRegistryGenerator:
    """Generates complete corporate registry with realistic structures"""
    
    def __init__(self):
        self.structure = CorporateStructureGraph()
        self.data_gen = RealisticDataGenerator()
    
    def generate_multi_level_structure(self, 
                                      num_holding_companies: int = 2,
                                      num_subsidiaries_per_holding: int = 3,
                                      num_sub_subsidiaries: int = 2) -> CorporateStructureGraph:
        """Generate a realistic multi-level corporate structure"""
        
        # Step 1: Create top-level beneficial owners
        ultimate_owners = []
        for _ in range(random.randint(2, 4)):
            person = self.data_gen.generate_person(
                nationality=random.choice(['US', 'UK', 'Singapore']),
                is_director=True
            )
            self.structure.add_person(person)
            ultimate_owners.append(person)
        
        # Step 2: Create offshore holding companies
        holding_companies = []
        for i in range(num_holding_companies):
            jurisdiction = random.choice([
                JurisdictionType.CAYMAN_ISLANDS,
                JurisdictionType.BVI,
                JurisdictionType.LUXEMBOURG
            ])
            
            holding = CorporateEntity(
                legal_name=self.data_gen.generate_company_name(),
                entity_type=EntityType.HOLDING_COMPANY,
                jurisdiction=jurisdiction,
                registration_number=self.data_gen.generate_registration_number(jurisdiction),
                registration_date=(datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d'),
                tax_id=self.data_gen.generate_tax_id(jurisdiction),
                business_address=self.data_gen.get_jurisdiction_address(jurisdiction),
                kyc_status='VERIFIED'
            )
            
            # Distribute ownership among ultimate owners
            ownership_percentages = self._distribute_ownership(len(ultimate_owners))
            for owner, percentage in zip(ultimate_owners, ownership_percentages):
                shareholder = Shareholder(
                    person_id=owner.person_id,
                    shares_issued=int(percentage * 10),
                    percentage_ownership=percentage,
                    is_beneficial_owner=True,
                    acquisition_date=holding.registration_date
                )
                holding.add_shareholder(shareholder)
            
            holding.beneficial_owners = [owner.person_id for owner in ultimate_owners]
            self.structure.add_entity(holding)
            holding_companies.append(holding)
        
        # Step 3: Create operating subsidiaries in different jurisdictions
        operating_companies = []
        for holding in holding_companies:
            for j in range(num_subsidiaries_per_holding):
                jurisdiction = random.choice([
                    JurisdictionType.US_STATE,
                    JurisdictionType.UK,
                    JurisdictionType.SINGAPORE,
                    JurisdictionType.HONG_KONG
                ])
                
                operating = CorporateEntity(
                    legal_name=self.data_gen.generate_company_name(),
                    entity_type=random.choice([EntityType.CORPORATION, EntityType.LLC, EntityType.SUBSIDIARY]),
                    jurisdiction=jurisdiction,
                    state_province='Delaware' if jurisdiction == JurisdictionType.US_STATE else None,
                    registration_number=self.data_gen.generate_registration_number(jurisdiction),
                    registration_date=(datetime.now() - timedelta(days=random.randint(200, 1095))).strftime('%Y-%m-%d'),
                    tax_id=self.data_gen.generate_tax_id(jurisdiction),
                    business_address=self.data_gen.get_jurisdiction_address(jurisdiction),
                    parent_entity_id=holding.entity_id,
                    kyc_status='VERIFIED'
                )
                
                # Add holding company as shareholder
                shareholder = Shareholder(
                    entity_id=holding.entity_id,
                    shares_issued=1000,
                    percentage_ownership=100.0,
                    is_beneficial_owner=False,
                    acquisition_date=operating.registration_date
                )
                operating.add_shareholder(shareholder)
                
                # Create control chain
                control_chain = ControlChain(
                    from_entity_id=holding.entity_id,
                    to_entity_id=operating.entity_id,
                    path=[holding.entity_id, operating.entity_id],
                    percentage_ownership=100.0,
                    control_type=OwnershipType.INDIRECT
                )
                self.structure.add_control_chain(control_chain)
                
                # Add directors
                for _ in range(random.randint(2, 4)):
                    director_person = self.data_gen.generate_person(nationality=random.choice(['US', 'UK', 'Singapore']))
                    self.structure.add_person(director_person)
                    
                    director = Director(
                        person_id=director_person.person_id,
                        title=random.choice(self.data_gen.TITLES),
                        appointment_date=operating.registration_date,
                        is_active=True,
                        signature_authority=random.random() > 0.3
                    )
                    operating.add_director(director)
                
                holding.subsidiary_entity_ids.append(operating.entity_id)
                self.structure.add_entity(operating)
                operating_companies.append(operating)
        
        # Step 4: Create sub-subsidiaries (special purpose vehicles, etc.)
        for operating in operating_companies[:len(operating_companies)//2]:  # Only for some operating companies
            for k in range(num_sub_subsidiaries):
                jurisdiction = random.choice([JurisdictionType.SINGAPORE, JurisdictionType.HONG_KONG, JurisdictionType.UK])
                
                sub_subsidiary = CorporateEntity(
                    legal_name=self.data_gen.generate_company_name(),
                    entity_type=EntityType.SPECIAL_PURPOSE_VEHICLE if random.random() > 0.5 else EntityType.SUBSIDIARY,
                    jurisdiction=jurisdiction,
                    registration_number=self.data_gen.generate_registration_number(jurisdiction),
                    registration_date=(datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                    tax_id=self.data_gen.generate_tax_id(jurisdiction),
                    business_address=self.data_gen.get_jurisdiction_address(jurisdiction),
                    parent_entity_id=operating.entity_id,
                    kyc_status='VERIFIED'
                )
                
                # Add operating company as shareholder
                shareholder = Shareholder(
                    entity_id=operating.entity_id,
                    shares_issued=500,
                    percentage_ownership=100.0,
                    is_beneficial_owner=False,
                    acquisition_date=sub_subsidiary.registration_date
                )
                sub_subsidiary.add_shareholder(shareholder)
                
                # Add to holding company's beneficial owners through control chain
                holding_of_operating = next(
                    (h for h in [c for c in self.structure.entities.values() 
                     if c.entity_id == operating.parent_entity_id]),
                    None
                )
                
                if holding_of_operating:
                    multi_level_chain = ControlChain(
                        from_entity_id=holding_of_operating.entity_id,
                        to_entity_id=sub_subsidiary.entity_id,
                        path=[holding_of_operating.entity_id, operating.entity_id, sub_subsidiary.entity_id],
                        percentage_ownership=100.0,
                        control_type=OwnershipType.INDIRECT
                    )
                    self.structure.add_control_chain(multi_level_chain)
                
                operating.subsidiary_entity_ids.append(sub_subsidiary.entity_id)
                self.structure.add_entity(sub_subsidiary)
        
        # Step 5: Add corporate documents
        self._generate_corporate_documents()
        
        return self.structure
    
    def _distribute_ownership(self, num_owners: int) -> List[float]:
        """Distribute ownership percentages among owners"""
        if num_owners == 1:
            return [100.0]
        elif num_owners == 2:
            split = random.choice([50.0, random.uniform(40, 60)])
            return [split, 100.0 - split]
        else:
            # Create unequal distribution
            base = 100.0 / num_owners
            percentages = [base + random.uniform(-base * 0.3, base * 0.3) for _ in range(num_owners)]
            total = sum(percentages)
            return [p * (100.0 / total) for p in percentages]
    
    def _generate_corporate_documents(self):
        """Generate corporate documents for all entities"""
        document_types = [
            DocumentType.ARTICLES_OF_INCORPORATION,
            DocumentType.BYLAWS,
            DocumentType.CERTIFICATE_OF_GOOD_STANDING,
            DocumentType.BOARD_RESOLUTION,
            DocumentType.SHAREHOLDERS_REGISTER,
            DocumentType.BENEFICIAL_OWNERSHIP_REGISTER,
            DocumentType.UBO_DECLARATION
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
    
    def generate_jurisdictional_network(self) -> CorporateStructureGraph:
        """Generate a network-style structure with cross-border relationships"""
        
        # Create entities in different jurisdictions
        jurisdictions = [
            JurisdictionType.CAYMAN_ISLANDS,
            JurisdictionType.LUXEMBOURG,
            JurisdictionType.SINGAPORE,
            JurisdictionType.UK,
            JurisdictionType.US_STATE,
            JurisdictionType.HONG_KONG
        ]
        
        entities_by_jurisdiction = {}
        
        # Create hub and spoke structure
        hub = CorporateEntity(
            legal_name="Global Coordination Hub Ltd",
            entity_type=EntityType.HOLDING_COMPANY,
            jurisdiction=JurisdictionType.LUXEMBOURG,
            registration_number=self.data_gen.generate_registration_number(JurisdictionType.LUXEMBOURG),
            registration_date=datetime.now().strftime('%Y-%m-%d'),
            tax_id=self.data_gen.generate_tax_id(JurisdictionType.LUXEMBOURG),
            business_address=self.data_gen.get_jurisdiction_address(JurisdictionType.LUXEMBOURG),
            kyc_status='VERIFIED'
        )
        
        # Add owner
        owner = self.data_gen.generate_person('Luxembourg')
        self.structure.add_person(owner)
        
        hub_shareholder = Shareholder(
            person_id=owner.person_id,
            shares_issued=1000,
            percentage_ownership=100.0,
            is_beneficial_owner=True,
            acquisition_date=hub.registration_date
        )
        hub.add_shareholder(hub_shareholder)
        hub.beneficial_owners = [owner.person_id]
        
        self.structure.add_entity(hub)
        entities_by_jurisdiction[JurisdictionType.LUXEMBOURG] = [hub]
        
        # Create spokes in other jurisdictions
        for jurisdiction in jurisdictions[1:]:
            entities = []
            for i in range(random.randint(2, 4)):
                entity = CorporateEntity(
                    legal_name=f"{self.data_gen.generate_company_name()}",
                    entity_type=random.choice([EntityType.CORPORATION, EntityType.SUBSIDIARY]),
                    jurisdiction=jurisdiction,
                    registration_number=self.data_gen.generate_registration_number(jurisdiction),
                    registration_date=(datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d'),
                    tax_id=self.data_gen.generate_tax_id(jurisdiction),
                    business_address=self.data_gen.get_jurisdiction_address(jurisdiction),
                    parent_entity_id=hub.entity_id if random.random() > 0.3 else None,
                    kyc_status='VERIFIED'
                )
                
                # Hub owns most, but allow some cross-ownership
                if random.random() > 0.4:
                    shareholder = Shareholder(
                        entity_id=hub.entity_id,
                        shares_issued=100,
                        percentage_ownership=random.uniform(50, 100),
                        is_beneficial_owner=False,
                        acquisition_date=entity.registration_date
                    )
                    entity.add_shareholder(shareholder)
                
                # Add some independent owners
                if random.random() > 0.6:
                    local_owner = self.data_gen.generate_person(nationality='US')
                    self.structure.add_person(local_owner)
                    
                    ind_shareholder = Shareholder(
                        person_id=local_owner.person_id,
                        shares_issued=50,
                        percentage_ownership=random.uniform(10, 50),
                        is_beneficial_owner=True,
                        acquisition_date=entity.registration_date
                    )
                    entity.add_shareholder(ind_shareholder)
                
                entities.append(entity)
                self.structure.add_entity(entity)
                hub.subsidiary_entity_ids.append(entity.entity_id)
            
            entities_by_jurisdiction[jurisdiction] = entities
        
        # Create cross-jurisdictional relationships
        all_entities = [e for entities in entities_by_jurisdiction.values() for e in entities]
        for entity in all_entities[1:]:  # Skip hub
            if random.random() > 0.7:
                # Create relationship with entity in another jurisdiction
                other_entity = random.choice([e for e in all_entities if e.entity_id != entity.entity_id])
                
                if random.random() > 0.5:
                    # Direct shareholding
                    shareholder = Shareholder(
                        entity_id=other_entity.entity_id,
                        shares_issued=random.randint(10, 100),
                        percentage_ownership=random.uniform(5, 40),
                        is_beneficial_owner=False
                    )
                    entity.add_shareholder(shareholder)
        
        self._generate_corporate_documents()
        return self.structure
    
    def generate_banking_group_structure(self) -> CorporateStructureGraph:
        """Generate a realistic banking group structure"""
        
        # Create holding company
        holding = CorporateEntity(
            legal_name="Global Financial Holdings plc",
            entity_type=EntityType.HOLDING_COMPANY,
            jurisdiction=JurisdictionType.UK,
            registration_number=self.data_gen.generate_registration_number(JurisdictionType.UK),
            registration_date="2015-03-15",
            tax_id=self.data_gen.generate_tax_id(JurisdictionType.UK),
            business_address=self.data_gen.get_jurisdiction_address(JurisdictionType.UK),
            kyc_status='VERIFIED'
        )
        
        # Create institutional shareholders
        institutional_owners = []
        owner_names = ['State Pension Fund', 'Insurance Company', 'Investment Manager', 'Sovereign Wealth Fund']
        for owner_name in owner_names:
            owner = CorporateEntity(
                legal_name=owner_name,
                entity_type=EntityType.INVESTMENT_FUND,
                jurisdiction=random.choice([JurisdictionType.CAYMAN_ISLANDS, JurisdictionType.LUXEMBOURG]),
                registration_number=self.data_gen.generate_registration_number(JurisdictionType.CAYMAN_ISLANDS),
                registration_date="2010-01-01",
                tax_id=self.data_gen.generate_tax_id(JurisdictionType.CAYMAN_ISLANDS),
                business_address=self.data_gen.get_jurisdiction_address(JurisdictionType.CAYMAN_ISLANDS),
                kyc_status='VERIFIED'
            )
            self.structure.add_entity(owner)
            institutional_owners.append(owner)
        
        # Distribute holding company ownership
        ownership_split = [30, 25, 25, 20]
        for owner, percentage in zip(institutional_owners, ownership_split):
            shareholder = Shareholder(
                entity_id=owner.entity_id,
                shares_issued=percentage,
                percentage_ownership=percentage,
                is_beneficial_owner=True
            )
            holding.add_shareholder(shareholder)
        
        self.structure.add_entity(holding)
        
        # Create banking subsidiaries
        bank_names = [
            "Global European Bank",
            "Global Asia-Pacific Bank",
            "Global Americas Bank",
            "Global Private Bank"
        ]
        
        for bank_name in bank_names:
            jurisdiction = random.choice([JurisdictionType.UK, JurisdictionType.CAYMAN_ISLANDS, JurisdictionType.SINGAPORE])
            
            bank = CorporateEntity(
                legal_name=bank_name,
                entity_type=EntityType.SUBSIDIARY,
                jurisdiction=jurisdiction,
                registration_number=self.data_gen.generate_registration_number(jurisdiction),
                registration_date=(datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                tax_id=self.data_gen.generate_tax_id(jurisdiction),
                business_address=self.data_gen.get_jurisdiction_address(jurisdiction),
                parent_entity_id=holding.entity_id,
                kyc_status='VERIFIED'
            )
            
            # Holding company owns bank
            shareholder = Shareholder(
                entity_id=holding.entity_id,
                shares_issued=1000,
                percentage_ownership=100.0,
                is_beneficial_owner=False
            )
            bank.add_shareholder(shareholder)
            
            # Add board of directors
            for _ in range(random.randint(3, 6)):
                director_person = self.data_gen.generate_person()
                self.structure.add_person(director_person)
                
                director = Director(
                    person_id=director_person.person_id,
                    title=random.choice(['Chairman', 'CEO', 'CFO', 'Director']),
                    appointment_date=bank.registration_date,
                    is_active=True,
                    signature_authority=True
                )
                bank.add_director(director)
            
            # Create control chain
            control_chain = ControlChain(
                from_entity_id=holding.entity_id,
                to_entity_id=bank.entity_id,
                path=[holding.entity_id, bank.entity_id],
                percentage_ownership=100.0,
                control_type=OwnershipType.INDIRECT
            )
            self.structure.add_control_chain(control_chain)
            
            holding.subsidiary_entity_ids.append(bank.entity_id)
            self.structure.add_entity(bank)
            
            # Create regional branches
            for _ in range(random.randint(2, 4)):
                region = random.choice(['North America', 'Europe', 'Asia', 'Middle East'])
                branch = CorporateEntity(
                    legal_name=f"{bank_name} - {region} Branch",
                    entity_type=EntityType.BRANCH,
                    jurisdiction=bank.jurisdiction,
                    registration_number=self.data_gen.generate_registration_number(bank.jurisdiction),
                    registration_date=bank.registration_date,
                    tax_id=self.data_gen.generate_tax_id(bank.jurisdiction),
                    business_address=self.data_gen.get_jurisdiction_address(bank.jurisdiction),
                    parent_entity_id=bank.entity_id,
                    kyc_status='VERIFIED'
                )
                
                shareholder = Shareholder(
                    entity_id=bank.entity_id,
                    shares_issued=500,
                    percentage_ownership=100.0,
                    is_beneficial_owner=False
                )
                branch.add_shareholder(shareholder)
                
                bank.subsidiary_entity_ids.append(branch.entity_id)
                self.structure.add_entity(branch)
        
        self._generate_corporate_documents()
        return self.structure


class RegistryExporter:
    """Export registry in various formats"""
    
    @staticmethod
    def export_to_json(structure: CorporateStructureGraph, filename: str = 'corporate_registry.json'):
        """Export structure to JSON"""
        export_data = {
            "registry_date": datetime.now().isoformat(),
            "summary": {
                "total_entities": len(structure.entities),
                "total_persons": len(structure.persons),
                "total_documents": len(structure.documents),
                "total_control_chains": len(structure.control_chains)
            },
            "entities": [],
            "persons": [],
            "control_chains": [],
            "documents": []
        }
        
        # Add entities
        for entity in structure.entities.values():
            entity_data = {
                "entity_id": entity.entity_id,
                "legal_name": entity.legal_name,
                "entity_type": entity.entity_type.value,
                "jurisdiction": entity.jurisdiction.value,
                "registration_number": entity.registration_number,
                "tax_id": entity.tax_id,
                "registration_date": entity.registration_date,
                "active_status": entity.active_status,
                "kyc_status": entity.kyc_status,
                "shareholders": [
                    {
                        "shareholder_id": s.shareholder_id,
                        "person_id": s.person_id,
                        "entity_id": s.entity_id,
                        "percentage_ownership": s.percentage_ownership,
                        "share_class": s.share_class
                    } for s in entity.shareholders
                ],
                "directors": [
                    {
                        "director_id": d.director_id,
                        "person_id": d.person_id,
                        "title": d.title,
                        "is_active": d.is_active,
                        "signature_authority": d.signature_authority
                    } for d in entity.directors
                ],
                "subsidiary_count": len(entity.subsidiary_entity_ids),
                "parent_entity_id": entity.parent_entity_id
            }
            export_data["entities"].append(entity_data)
        
        # Add persons
        for person in structure.persons.values():
            person_data = {
                "person_id": person.person_id,
                "full_name": person.get_full_name(),
                "nationality": person.nationality,
                "kyc_status": person.kyc_status,
                "pep_status": person.pep_status,
                "sanctions_status": person.sanctions_status,
                "email": person.email
            }
            export_data["persons"].append(person_data)
        
        # Add control chains
        for chain in structure.control_chains.values():
            chain_data = {
                "chain_id": chain.chain_id,
                "from_entity_id": chain.from_entity_id,
                "to_entity_id": chain.to_entity_id,
                "depth": chain.get_depth(),
                "percentage_ownership": chain.percentage_ownership,
                "control_type": chain.control_type.value
            }
            export_data["control_chains"].append(chain_data)
        
        # Add documents
        for doc in structure.documents.values():
            doc_data = {
                "document_id": doc.document_id,
                "entity_id": doc.entity_id,
                "document_type": doc.document_type.value,
                "jurisdiction": doc.jurisdiction.value,
                "approval_status": doc.approval_status,
                "compliance_verified": doc.compliance_verified
            }
            export_data["documents"].append(doc_data)
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    @staticmethod
    def export_to_csv(structure: CorporateStructureGraph, prefix: str = 'registry'):
        """Export structure to CSV files"""
        import csv
        
        # Entities CSV
        with open(f'{prefix}_entities.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'entity_id', 'legal_name', 'entity_type', 'jurisdiction',
                'registration_number', 'tax_id', 'kyc_status', 'active_status'
            ])
            writer.writeheader()
            for entity in structure.entities.values():
                writer.writerow({
                    'entity_id': entity.entity_id,
                    'legal_name': entity.legal_name,
                    'entity_type': entity.entity_type.value,
                    'jurisdiction': entity.jurisdiction.value,
                    'registration_number': entity.registration_number,
                    'tax_id': entity.tax_id,
                    'kyc_status': entity.kyc_status,
                    'active_status': entity.active_status
                })
        
        # Persons CSV
        with open(f'{prefix}_persons.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'person_id', 'full_name', 'nationality', 'kyc_status', 'pep_status', 'email'
            ])
            writer.writeheader()
            for person in structure.persons.values():
                writer.writerow({
                    'person_id': person.person_id,
                    'full_name': person.get_full_name(),
                    'nationality': person.nationality,
                    'kyc_status': person.kyc_status,
                    'pep_status': person.pep_status,
                    'email': person.email
                })
        
        # Shareholders CSV
        with open(f'{prefix}_shareholders.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'entity_id', 'shareholder_id', 'person_id', 'entity_id_owner',
                'percentage_ownership', 'share_class', 'is_beneficial_owner'
            ])
            writer.writeheader()
            for entity in structure.entities.values():
                for shareholder in entity.shareholders:
                    writer.writerow({
                        'entity_id': entity.entity_id,
                        'shareholder_id': shareholder.shareholder_id,
                        'person_id': shareholder.person_id,
                        'entity_id_owner': shareholder.entity_id,
                        'percentage_ownership': shareholder.percentage_ownership,
                        'share_class': shareholder.share_class,
                        'is_beneficial_owner': shareholder.is_beneficial_owner
                    })
        
        # Directors CSV
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
        
        return [f'{prefix}_entities.csv', f'{prefix}_persons.csv', 
                f'{prefix}_shareholders.csv', f'{prefix}_directors.csv']
    
    @staticmethod
    def generate_compliance_report(structure: CorporateStructureGraph) -> str:
        """Generate a compliance report"""
        report = []
        report.append("=" * 80)
        report.append("CORPORATE REGISTRY COMPLIANCE REPORT")
        report.append("=" * 80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Summary statistics
        report.append("SUMMARY STATISTICS")
        report.append("-" * 80)
        report.append(f"Total Entities: {len(structure.entities)}")
        report.append(f"Total Persons: {len(structure.persons)}")
        report.append(f"Total Documents: {len(structure.documents)}")
        report.append(f"Total Control Chains: {len(structure.control_chains)}\n")
        
        # Jurisdiction breakdown
        report.append("JURISDICTION BREAKDOWN")
        report.append("-" * 80)
        jurisdiction_summary = structure.get_multi_jurisdiction_summary()
        for juris, data in sorted(jurisdiction_summary.items()):
            report.append(f"\n{juris}:")
            report.append(f"  Entities: {data['entity_count']}")
            report.append(f"  KYC Status: {data['kyc_status']}")
        
        # KYC Status Summary
        report.append("\n\nKYC STATUS SUMMARY")
        report.append("-" * 80)
        kyc_summary = {'VERIFIED': 0, 'PENDING': 0, 'REJECTED': 0}
        for entity in structure.entities.values():
            kyc_summary[entity.kyc_status] = kyc_summary.get(entity.kyc_status, 0) + 1
        
        for status, count in kyc_summary.items():
            report.append(f"{status}: {count}")
        
        # PEP and Sanctions Check
        report.append("\n\nPEP & SANCTIONS CHECK")
        report.append("-" * 80)
        pep_persons = [p for p in structure.persons.values() if p.pep_status]
        sanctions_persons = [p for p in structure.persons.values() if p.sanctions_status]
        
        report.append(f"PEP Persons: {len(pep_persons)}")
        if pep_persons:
            for person in pep_persons:
                report.append(f"  - {person.get_full_name()} ({person.nationality})")
        
        report.append(f"\nSanctions Persons: {len(sanctions_persons)}")
        if sanctions_persons:
            for person in sanctions_persons:
                report.append(f"  - {person.get_full_name()} ({person.nationality})")
        
        # Control Chain Integrity
        report.append("\n\nCONTROL CHAIN INTEGRITY")
        report.append("-" * 80)
        issues = structure.verify_control_chain_integrity()
        if issues:
            report.append(f"Issues Found: {len(issues)}")
            for issue in issues:
                report.append(f"  ⚠ {issue}")
        else:
            report.append("✓ All control chains verified")
        
        report.append("\n" + "=" * 80 + "\n")
        
        return "\n".join(report)


# Main execution
if __name__ == "__main__":
    print("Generating comprehensive corporate registry...\n")
    
    # Generator 1: Multi-level structure
    print("1. Generating multi-level holding company structure...")
    gen1 = CorporateRegistryGenerator()
    structure1 = gen1.generate_multi_level_structure(
        num_holding_companies=2,
        num_subsidiaries_per_holding=3,
        num_sub_subsidiaries=2
    )
    
    print(f"   ✓ Created {len(structure1.entities)} entities across {len(set(e.jurisdiction for e in structure1.entities.values()))} jurisdictions")
    print(f"   ✓ Created {len(structure1.persons)} persons with KYC records")
    print(f"   ✓ Created {len(structure1.documents)} corporate documents")
    
    # Generator 2: Banking group
    print("\n2. Generating banking group structure...")
    gen2 = CorporateRegistryGenerator()
    structure2 = gen2.generate_banking_group_structure()
    
    print(f"   ✓ Created {len(structure2.entities)} entities (holding + 4 banks + branches)")
    print(f"   ✓ Created {len(structure2.persons)} banking professionals")
    
    # Export Registry 1
    print("\n3. Exporting multi-level structure...")
    exporter = RegistryExporter()
    json_file = exporter.export_to_json(structure1, 'multilevel_registry.json')
    csv_files = exporter.export_to_csv(structure1, 'multilevel_registry')
    print(f"   ✓ Exported to {json_file}")
    print(f"   ✓ Exported to {csv_files}")
    
    # Generate compliance report for Structure 1
    print("\n4. Generating compliance report...")
    report = exporter.generate_compliance_report(structure1)
    print(report)
    
    # Save report
    with open('multilevel_compliance_report.txt', 'w') as f:
        f.write(report)
    print("   ✓ Report saved to multilevel_compliance_report.txt")
    
    # Show sample hierarchy
    print("\n5. Sample Ownership Hierarchy:")
    print("-" * 80)
    
    # Get first operating company
    operating_companies = [e for e in structure1.entities.values() 
                          if e.entity_type == EntityType.LLC or e.entity_type == EntityType.SUBSIDIARY]
    if operating_companies:
        sample_entity = operating_companies[0]
        hierarchy = structure1.get_ownership_hierarchy(sample_entity.entity_id)
        print(f"\nEntity: {hierarchy['entity']['legal_name']}")
        print(f"Jurisdiction: {hierarchy['entity']['jurisdiction']}")
        print(f"KYC Status: {hierarchy['entity']['kyc_status']}")
        
        if hierarchy['shareholders']:
            print(f"\nDirect Shareholders:")
            for sh in hierarchy['shareholders'][:3]:
                print(f"  - {sh['name']} ({sh['type']}): {sh['percentage']:.1f}%")
        
        if hierarchy['indirect_owners']:
            print(f"\nIndirect Ownership:")
            for io in hierarchy['indirect_owners'][:2]:
                print(f"  - Chain depth: {io['depth']} levels, Ownership: {io['percentage']:.1f}%")
        
        if hierarchy['ultimate_beneficial_owners']:
            print(f"\nUltimate Beneficial Owners:")
            for ubo in hierarchy['ultimate_beneficial_owners'][:3]:
                print(f"  - {ubo['name']} ({ubo['type']})")
    
    print("\n" + "=" * 80)
    print("Corporate registry generation complete!")
    print("=" * 80)
