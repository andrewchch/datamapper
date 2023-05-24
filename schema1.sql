-- CourseDefinition table
CREATE TABLE CourseDefinition (
    CourseDefinitionID INT PRIMARY KEY,
    AbbrTitle VARCHAR(255),
    CourseCode VARCHAR(255),
    CourseFactor DECIMAL(10, 2),
    EqCreditValue INT,
    ExtractToWeb INT,
    MaxEnrolments INT,
    MinEnrolments INT,
    Stage INT,
    StartDate DATETIME,
    EndDate DATETIME,
    CourseTitle VARCHAR(255),
    CostCategoryID INT,
    DeliveryModeID INT,
    EducationInstituteID INT,
    NZSCEDCategoryID INT,
    ProgrammeIDOwning INT,
    SourceOfFundingID INT,
    CourseDefinitionStatusID INT,
    CourseDefinitionSubstatusID INT,
    CourseDesc VARCHAR(MAX),
    OrgUnitIDOwning INT,
    IsThesisCourse INT
);

-- CostCategory table
CREATE TABLE CostCategory (
    CostCategoryID INT PRIMARY KEY,
    -- Add columns for CostCategory attributes
);

-- DeliveryMode table
CREATE TABLE DeliveryMode (
    DeliveryModeID INT PRIMARY KEY,
    -- Add columns for DeliveryMode attributes
);

-- EducationInstitute table
CREATE TABLE EducationInstitute (
    EducationInstituteID INT PRIMARY KEY,
    -- Add columns for EducationInstitute attributes
);

-- NZSCEDCategory table
CREATE TABLE NZSCEDCategory (
    NZSCEDCategoryID INT PRIMARY KEY,
    -- Add columns for NZSCEDCategory attributes
);

-- Programme table
CREATE TABLE Programme (
    ProgrammeID INT PRIMARY KEY,
    -- Add columns for Programme attributes
);

-- SourceOfFunding table
CREATE TABLE SourceOfFunding (
    SourceOfFundingID INT PRIMARY KEY,
    -- Add columns for SourceOfFunding attributes
);

-- CourseDefinitionStatus table
CREATE TABLE CourseDefinitionStatus (
    CourseDefinitionStatusID INT PRIMARY KEY,
    -- Add columns for CourseDefinitionStatus attributes
);

-- CourseDefinitionSubstatus table
CREATE TABLE CourseDefinitionSubstatus (
    CourseDefinitionSubstatusID INT PRIMARY KEY,
    -- Add columns for CourseDefinitionSubstatus attributes
);

-- OrgUnit table
CREATE TABLE OrgUnit (
    OrgUnitID INT PRIMARY KEY,
    -- Add columns for OrgUnit attributes
);

-- Add foreign key constraints

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (CostCategoryID) REFERENCES CostCategory(CostCategoryID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (DeliveryModeID) REFERENCES DeliveryMode(DeliveryModeID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (EducationInstituteID) REFERENCES EducationInstitute(EducationInstituteID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (NZSCEDCategoryID) REFERENCES NZSCEDCategory(NZSCEDCategoryID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (ProgrammeIDOwning) REFERENCES Programme(ProgrammeID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (SourceOfFundingID) REFERENCES SourceOfFunding(SourceOfFundingID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (CourseDefinitionStatusID) REFERENCES CourseDefinitionStatus(CourseDefinitionStatusID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (CourseDefinitionSubstatusID) REFERENCES CourseDefinitionSubstatus(CourseDefinitionSubstatusID);

ALTER TABLE CourseDefinition
ADD FOREIGN KEY (OrgUnitIDOwning) REFERENCES OrgUnit(OrgUnitID);