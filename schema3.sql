-- CourseDefinition table
CREATE TABLE CourseDefinition (
  CourseDefinitionID INT PRIMARY KEY,
  AbbrTitle VARCHAR(255),
  CourseCode VARCHAR(255),
  CourseFactor DECIMAL(10, 4),
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
  CourseDesc TEXT,
  OrgUnitIDOwning INT,
  IsThesisCourse INT,
  FOREIGN KEY (CostCategoryID) REFERENCES CostCategory(CostCategoryID),
  FOREIGN KEY (DeliveryModeID) REFERENCES DeliveryMode(DeliveryModeID),
  FOREIGN KEY (EducationInstituteID) REFERENCES EducationInstitute(EducationInstituteID),
  FOREIGN KEY (NZSCEDCategoryID) REFERENCES NZSCEDCategory(NZSCEDCategoryID),
  FOREIGN KEY (ProgrammeIDOwning) REFERENCES Programme(ProgrammeID),
  FOREIGN KEY (SourceOfFundingID) REFERENCES SourceOfFunding(SourceOfFundingID),
  FOREIGN KEY (CourseDefinitionStatusID) REFERENCES CourseDefinitionStatus(CourseDefinitionStatusID),
  FOREIGN KEY (CourseDefinitionSubstatusID) REFERENCES CourseDefinitionSubstatus(CourseDefinitionSubstatusID),
  FOREIGN KEY (OrgUnitIDOwning) REFERENCES OrgUnit(OrgUnitID)
);

-- CostCategory table
CREATE TABLE CostCategory (
  CostCategoryID INT PRIMARY KEY,
  CostCategoryName VARCHAR(255)
);

-- DeliveryMode table
CREATE TABLE DeliveryMode (
  DeliveryModeID INT PRIMARY KEY,
  DeliveryModeName VARCHAR(255)
);

-- EducationInstitute table
CREATE TABLE EducationInstitute (
  EducationInstituteID INT PRIMARY KEY,
  InstituteName VARCHAR(255)
);

-- NZSCEDCategory table
CREATE TABLE NZSCEDCategory (
  NZSCEDCategoryID INT PRIMARY KEY,
  CategoryName VARCHAR(255)
);

-- Programme table
CREATE TABLE Programme (
  ProgrammeID INT PRIMARY KEY,
  ProgrammeName VARCHAR(255)
);

-- SourceOfFunding table
CREATE TABLE SourceOfFunding (
  SourceOfFundingID INT PRIMARY KEY,
  FundingSourceName VARCHAR(255)
);

-- CourseDefinitionStatus table
CREATE TABLE CourseDefinitionStatus (
  CourseDefinitionStatusID INT PRIMARY KEY,
  StatusName VARCHAR(255)
);

-- CourseDefinitionSubstatus table
CREATE TABLE CourseDefinitionSubstatus (
  CourseDefinitionSubstatusID INT PRIMARY KEY,
  SubstatusName VARCHAR(255)
);

-- OrgUnit table
CREATE TABLE OrgUnit (
  OrgUnitID INT PRIMARY KEY,
  OrgUnitName VARCHAR(255)
);