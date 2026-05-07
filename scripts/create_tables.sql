/*
Run this after scripts/create_db.sql.
This script is intentionally simple and idempotent where practical.
*/

USE [ezeas-intelligence-db];
GO

IF OBJECT_ID(N'dbo.KnowledgeDocument', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.KnowledgeDocument (
        KnowledgeDocumentId NVARCHAR(36) NOT NULL PRIMARY KEY,
        TenantId NVARCHAR(100) NULL,
        SourceType NVARCHAR(50) NOT NULL,
        SourceAuthority INT NOT NULL,
        CapabilityStatus NVARCHAR(50) NULL,
        OriginalFileName NVARCHAR(255) NOT NULL,
        StoredFilePath NVARCHAR(1000) NULL,
        FileExtension NVARCHAR(20) NOT NULL,
        FileSha256 NVARCHAR(64) NOT NULL,
        Title NVARCHAR(255) NULL,
        DocumentStatus NVARCHAR(50) NOT NULL CONSTRAINT DF_KnowledgeDocument_DocumentStatus DEFAULT 'ACTIVE',
        ExtractedTextLength INT NOT NULL,
        ChunkCount INT NOT NULL,
        CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_KnowledgeDocument_CreatedAt DEFAULT SYSUTCDATETIME(),
        UpdatedAt DATETIME2 NULL
    );
END;
GO

IF OBJECT_ID(N'dbo.KnowledgeChunk', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.KnowledgeChunk (
        KnowledgeChunkId NVARCHAR(36) NOT NULL PRIMARY KEY,
        KnowledgeDocumentId NVARCHAR(36) NOT NULL,
        ChunkIndex INT NOT NULL,
        ChunkText NVARCHAR(MAX) NOT NULL,
        ChunkHash NVARCHAR(64) NOT NULL,
        SourcePage INT NULL,
        SourceSection NVARCHAR(255) NULL,
        TokenEstimate INT NULL,
        CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_KnowledgeChunk_CreatedAt DEFAULT SYSUTCDATETIME(),
        CONSTRAINT FK_KnowledgeChunk_KnowledgeDocument FOREIGN KEY (KnowledgeDocumentId)
            REFERENCES dbo.KnowledgeDocument(KnowledgeDocumentId)
    );
END;
GO

IF OBJECT_ID(N'dbo.KnowledgeChatSession', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.KnowledgeChatSession (
        KnowledgeChatSessionId NVARCHAR(36) NOT NULL PRIMARY KEY,
        TenantId NVARCHAR(100) NULL,
        UserId NVARCHAR(100) NULL,
        Title NVARCHAR(255) NULL,
        CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_KnowledgeChatSession_CreatedAt DEFAULT SYSUTCDATETIME(),
        UpdatedAt DATETIME2 NULL
    );
END;
GO

IF OBJECT_ID(N'dbo.KnowledgeChatMessage', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.KnowledgeChatMessage (
        KnowledgeChatMessageId NVARCHAR(36) NOT NULL PRIMARY KEY,
        KnowledgeChatSessionId NVARCHAR(36) NOT NULL,
        Role NVARCHAR(20) NOT NULL,
        Content NVARCHAR(MAX) NOT NULL,
        CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_KnowledgeChatMessage_CreatedAt DEFAULT SYSUTCDATETIME(),
        CONSTRAINT FK_KnowledgeChatMessage_KnowledgeChatSession FOREIGN KEY (KnowledgeChatSessionId)
            REFERENCES dbo.KnowledgeChatSession(KnowledgeChatSessionId)
    );
END;
GO

IF OBJECT_ID(N'dbo.AIInteractionAudit', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.AIInteractionAudit (
        AIInteractionAuditId NVARCHAR(36) NOT NULL PRIMARY KEY,
        TenantId NVARCHAR(100) NULL,
        UserId NVARCHAR(100) NULL,
        KnowledgeChatSessionId NVARCHAR(36) NULL,
        UserQuestion NVARCHAR(MAX) NOT NULL,
        RetrievedChunkIdsJson NVARCHAR(MAX) NOT NULL,
        RetrievedDocumentIdsJson NVARCHAR(MAX) NOT NULL,
        SourceReferencesJson NVARCHAR(MAX) NOT NULL,
        ModelName NVARCHAR(100) NOT NULL,
        PromptPolicy NVARCHAR(100) NOT NULL,
        ResponseText NVARCHAR(MAX) NOT NULL,
        CreatedAt DATETIME2 NOT NULL CONSTRAINT DF_AIInteractionAudit_CreatedAt DEFAULT SYSUTCDATETIME(),
        CONSTRAINT FK_AIInteractionAudit_KnowledgeChatSession FOREIGN KEY (KnowledgeChatSessionId)
            REFERENCES dbo.KnowledgeChatSession(KnowledgeChatSessionId)
    );
END;
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_KnowledgeDocument_FileSha256')
    CREATE UNIQUE INDEX IX_KnowledgeDocument_FileSha256 ON dbo.KnowledgeDocument(FileSha256);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_KnowledgeDocument_SourceType')
    CREATE INDEX IX_KnowledgeDocument_SourceType ON dbo.KnowledgeDocument(SourceType);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_KnowledgeChunk_KnowledgeDocumentId')
    CREATE INDEX IX_KnowledgeChunk_KnowledgeDocumentId ON dbo.KnowledgeChunk(KnowledgeDocumentId);
GO
