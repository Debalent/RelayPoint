"""
Elite Workflow Template Library

This module provides pre-built workflow templates that address common
business use cases based on user feedback and survey responses.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

from ..workflow_engine_elite import WorkflowDefinition, StepConfiguration, StepType, WorkflowVariable


@dataclass
class WorkflowTemplate:
    """Pre-built workflow template."""
    id: str
    name: str
    description: str
    category: str
    difficulty: str  # "beginner", "intermediate", "advanced"
    estimated_time: str
    use_cases: List[str]
    prerequisites: List[str]
    workflow_definition: WorkflowDefinition
    customization_tips: List[str]


class EliteTemplateLibrary:
    """
    Comprehensive library of pre-built workflow templates addressing
    common user needs and survey feedback.
    """
    
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize all pre-built templates."""
        
        # Customer Onboarding Template
        self.templates["customer_onboarding"] = self._create_customer_onboarding_template()
        
        # Invoice Processing Template
        self.templates["invoice_processing"] = self._create_invoice_processing_template()
        
        # Lead Qualification Template
        self.templates["lead_qualification"] = self._create_lead_qualification_template()
        
        # Data Backup & Sync Template
        self.templates["data_backup_sync"] = self._create_data_backup_template()
        
        # Employee Onboarding Template
        self.templates["employee_onboarding"] = self._create_employee_onboarding_template()
        
        # Social Media Management Template
        self.templates["social_media"] = self._create_social_media_template()
        
        # E-commerce Order Processing Template
        self.templates["ecommerce_orders"] = self._create_ecommerce_template()
        
        # Support Ticket Management Template
        self.templates["support_tickets"] = self._create_support_ticket_template()
        
        # Content Creation Pipeline Template
        self.templates["content_creation"] = self._create_content_creation_template()
        
        # Financial Reporting Template
        self.templates["financial_reporting"] = self._create_financial_reporting_template()
    
    def _create_customer_onboarding_template(self) -> WorkflowTemplate:
        """Create customer onboarding workflow template."""
        
        # Define workflow steps
        steps = [
            StepConfiguration(
                step_id="start",
                step_type=StepType.START,
                name="Customer Signup Trigger",
                description="Triggered when new customer signs up",
                config={},
                outputs={"customer_data": "customer_info"}
            ),
            StepConfiguration(
                step_id="send_welcome_email",
                step_type=StepType.EMAIL_SEND,
                name="Send Welcome Email",
                description="Send personalized welcome email to new customer",
                config={
                    "to": "{{customer_info.email}}",
                    "template": "welcome_template",
                    "personalization": {
                        "first_name": "{{customer_info.first_name}}",
                        "company": "{{customer_info.company}}"
                    }
                },
                depends_on=["start"]
            ),
            StepConfiguration(
                step_id="create_crm_record",
                step_type=StepType.HTTP_REQUEST,
                name="Create CRM Record",
                description="Add customer to CRM system",
                config={
                    "method": "POST",
                    "url": "{{crm_api_url}}/contacts",
                    "headers": {
                        "Authorization": "Bearer {{crm_api_token}}",
                        "Content-Type": "application/json"
                    },
                    "data": {
                        "email": "{{customer_info.email}}",
                        "first_name": "{{customer_info.first_name}}",
                        "last_name": "{{customer_info.last_name}}",
                        "company": "{{customer_info.company}}",
                        "source": "website_signup"
                    }
                },
                depends_on=["start"],
                outputs={"crm_record_id": "crm_id"}
            ),
            StepConfiguration(
                step_id="schedule_onboarding_call",
                step_type=StepType.HTTP_REQUEST,
                name="Schedule Onboarding Call",
                description="Automatically schedule onboarding call",
                config={
                    "method": "POST",
                    "url": "{{calendar_api_url}}/events",
                    "headers": {
                        "Authorization": "Bearer {{calendar_api_token}}"
                    },
                    "data": {
                        "title": "Onboarding Call - {{customer_info.first_name}} {{customer_info.last_name}}",
                        "duration": 30,
                        "attendees": ["{{customer_info.email}}", "onboarding@company.com"],
                        "auto_schedule": True
                    }
                },
                depends_on=["create_crm_record"]
            ),
            StepConfiguration(
                step_id="add_to_onboarding_sequence",
                step_type=StepType.HTTP_REQUEST,
                name="Add to Email Sequence",
                description="Add customer to automated email sequence",
                config={
                    "method": "POST",
                    "url": "{{email_platform_url}}/sequences/onboarding/subscribers",
                    "data": {
                        "email": "{{customer_info.email}}",
                        "custom_fields": {
                            "first_name": "{{customer_info.first_name}}",
                            "company": "{{customer_info.company}}",
                            "signup_date": "{{current_date}}"
                        }
                    }
                },
                depends_on=["send_welcome_email"]
            ),
            StepConfiguration(
                step_id="notify_sales_team",
                step_type=StepType.WEBHOOK,
                name="Notify Sales Team",
                description="Send notification to sales team via Slack",
                config={
                    "url": "{{slack_webhook_url}}",
                    "payload": {
                        "text": "🎉 New customer signup: {{customer_info.first_name}} {{customer_info.last_name}} from {{customer_info.company}}",
                        "channel": "#sales",
                        "attachments": [
                            {
                                "color": "good",
                                "fields": [
                                    {"title": "Email", "value": "{{customer_info.email}}", "short": True},
                                    {"title": "Company", "value": "{{customer_info.company}}", "short": True},
                                    {"title": "CRM ID", "value": "{{crm_id}}", "short": True}
                                ]
                            }
                        ]
                    }
                },
                depends_on=["create_crm_record"]
            ),
            StepConfiguration(
                step_id="end",
                step_type=StepType.END,
                name="Onboarding Complete",
                description="Customer onboarding workflow completed",
                config={},
                depends_on=["schedule_onboarding_call", "add_to_onboarding_sequence", "notify_sales_team"]
            )
        ]
        
        # Define workflow variables
        variables = {
            "customer_info": WorkflowVariable(
                name="customer_info",
                value={},
                type="object",
                description="Customer information from signup form"
            ),
            "crm_api_url": WorkflowVariable(
                name="crm_api_url",
                value="https://api.salesforce.com/services/data/v52.0",
                type="string",
                description="CRM API endpoint URL"
            ),
            "crm_api_token": WorkflowVariable(
                name="crm_api_token",
                value="",
                type="string",
                description="CRM API authentication token",
                encrypted=True
            ),
            "calendar_api_url": WorkflowVariable(
                name="calendar_api_url",
                value="https://api.calendly.com/scheduled_events",
                type="string",
                description="Calendar API endpoint"
            ),
            "email_platform_url": WorkflowVariable(
                name="email_platform_url",
                value="https://api.mailchimp.com/3.0",
                type="string",
                description="Email platform API URL"
            ),
            "slack_webhook_url": WorkflowVariable(
                name="slack_webhook_url",
                value="",
                type="string",
                description="Slack webhook URL for notifications",
                encrypted=True
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="customer_onboarding_v1",
            name="Customer Onboarding Automation",
            description="Automated customer onboarding workflow with CRM integration, email sequences, and team notifications",
            version="1.0.0",
            nodes=[],  # Will be converted from steps
            edges=[],  # Will be generated from dependencies
            variables=variables,
            settings={
                "created_by": "template_library",
                "template": True,
                "category": "sales_marketing"
            }
        )
        
        return WorkflowTemplate(
            id="customer_onboarding",
            name="Customer Onboarding Automation",
            description="Complete customer onboarding workflow with CRM integration, automated emails, and team notifications",
            category="Sales & Marketing",
            difficulty="intermediate",
            estimated_time="15-30 minutes setup",
            use_cases=[
                "SaaS customer onboarding",
                "E-commerce customer welcome",
                "Service business client setup",
                "B2B lead conversion"
            ],
            prerequisites=[
                "CRM system with API access (Salesforce, HubSpot, Pipedrive)",
                "Email marketing platform (Mailchimp, ConvertKit, ActiveCampaign)",
                "Calendar scheduling tool (Calendly, Acuity)",
                "Slack workspace for notifications"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Customize email templates to match your brand",
                "Adjust onboarding call duration based on your needs",
                "Add conditional logic based on customer type or plan",
                "Include additional integrations like help desk or billing systems",
                "Set up A/B testing for different onboarding sequences"
            ]
        )
    
    def _create_invoice_processing_template(self) -> WorkflowTemplate:
        """Create automated invoice processing template."""
        
        variables = {
            "invoice_data": WorkflowVariable(
                name="invoice_data",
                value={},
                type="object",
                description="Invoice data from uploaded document"
            ),
            "approval_threshold": WorkflowVariable(
                name="approval_threshold",
                value=5000.00,
                type="number",
                description="Amount threshold requiring approval"
            ),
            "accounting_system_url": WorkflowVariable(
                name="accounting_system_url",
                value="https://api.quickbooks.com/v3",
                type="string",
                description="Accounting system API endpoint"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="invoice_processing_v1",
            name="Automated Invoice Processing",
            description="AI-powered invoice processing with approval workflows and accounting integration",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "finance"}
        )
        
        return WorkflowTemplate(
            id="invoice_processing",
            name="Automated Invoice Processing",
            description="AI-powered invoice processing with OCR, approval workflows, and accounting system integration",
            category="Finance & Accounting",
            difficulty="advanced",
            estimated_time="30-45 minutes setup",
            use_cases=[
                "Accounts payable automation",
                "Vendor invoice processing",
                "Expense report automation",
                "Financial document management"
            ],
            prerequisites=[
                "Accounting system with API (QuickBooks, Xero, NetSuite)",
                "Document storage (Google Drive, SharePoint, Dropbox)",
                "Email system for approvals",
                "OCR service or AI document processing"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Configure OCR accuracy thresholds",
                "Set up multiple approval levels based on amount",
                "Add vendor validation and duplicate checking",
                "Include payment scheduling automation",
                "Set up exception handling for manual review"
            ]
        )
    
    def _create_lead_qualification_template(self) -> WorkflowTemplate:
        """Create lead qualification and scoring template."""
        
        variables = {
            "lead_data": WorkflowVariable(
                name="lead_data",
                value={},
                type="object",
                description="Lead information from form or import"
            ),
            "scoring_criteria": WorkflowVariable(
                name="scoring_criteria",
                value={
                    "company_size": {"weight": 0.3, "ranges": {"1-10": 1, "11-50": 3, "51-200": 5, "200+": 8}},
                    "industry": {"weight": 0.2, "values": {"technology": 8, "healthcare": 7, "finance": 6}},
                    "budget": {"weight": 0.4, "ranges": {"<1k": 1, "1k-10k": 5, "10k-50k": 8, "50k+": 10}},
                    "timeline": {"weight": 0.1, "values": {"immediate": 10, "3months": 7, "6months": 4, "future": 1}}
                },
                type="object",
                description="Lead scoring criteria and weights"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="lead_qualification_v1",
            name="AI-Powered Lead Qualification",
            description="Automated lead scoring, qualification, and routing based on AI analysis",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "sales_marketing"}
        )
        
        return WorkflowTemplate(
            id="lead_qualification",
            name="AI-Powered Lead Qualification",
            description="Intelligent lead scoring, qualification, and automated routing to appropriate sales reps",
            category="Sales & Marketing",
            difficulty="intermediate",
            estimated_time="20-30 minutes setup",
            use_cases=[
                "Inbound lead qualification",
                "Trade show lead processing",
                "Marketing qualified lead (MQL) scoring",
                "Sales rep assignment automation"
            ],
            prerequisites=[
                "CRM system integration",
                "Lead capture forms or systems",
                "Sales team contact information",
                "Scoring criteria definitions"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Customize scoring criteria for your industry",
                "Set up multiple qualification tiers",
                "Add enrichment data from third-party sources",
                "Configure different routing rules by territory",
                "Include lead nurturing sequences for low-score leads"
            ]
        )
    
    def _create_data_backup_template(self) -> WorkflowTemplate:
        """Create automated data backup and sync template."""
        
        variables = {
            "backup_sources": WorkflowVariable(
                name="backup_sources",
                value=[],
                type="array",
                description="List of data sources to backup"
            ),
            "backup_destination": WorkflowVariable(
                name="backup_destination",
                value="",
                type="string",
                description="Primary backup storage location"
            ),
            "retention_days": WorkflowVariable(
                name="retention_days",
                value=30,
                type="number",
                description="Number of days to retain backups"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="data_backup_v1",
            name="Automated Data Backup & Sync",
            description="Comprehensive data backup automation with multiple storage options and retention policies",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "operations"}
        )
        
        return WorkflowTemplate(
            id="data_backup_sync",
            name="Automated Data Backup & Sync",
            description="Comprehensive backup automation with multi-cloud storage, versioning, and disaster recovery",
            category="IT Operations",
            difficulty="advanced",
            estimated_time="45-60 minutes setup",
            use_cases=[
                "Database backup automation",
                "File system synchronization",
                "Cloud storage backup",
                "Disaster recovery preparation"
            ],
            prerequisites=[
                "Cloud storage accounts (AWS S3, Google Cloud, Azure)",
                "Database access credentials",
                "File system permissions",
                "Monitoring and alerting systems"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Set up incremental vs full backup schedules",
                "Configure encryption for sensitive data",
                "Add integrity checks and verification",
                "Set up multiple backup destinations",
                "Include automated restore testing"
            ]
        )
    
    def _create_employee_onboarding_template(self) -> WorkflowTemplate:
        """Create employee onboarding workflow template."""
        
        variables = {
            "employee_data": WorkflowVariable(
                name="employee_data",
                value={},
                type="object",
                description="New employee information"
            ),
            "department": WorkflowVariable(
                name="department",
                value="",
                type="string",
                description="Employee department for role-specific onboarding"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="employee_onboarding_v1",
            name="Employee Onboarding Automation",
            description="Complete employee onboarding with account setup, training, and compliance",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "hr"}
        )
        
        return WorkflowTemplate(
            id="employee_onboarding",
            name="Employee Onboarding Automation",
            description="Streamlined employee onboarding with account provisioning, training assignments, and compliance tracking",
            category="Human Resources",
            difficulty="intermediate",
            estimated_time="30-40 minutes setup",
            use_cases=[
                "New hire onboarding",
                "Contractor setup",
                "Role changes and transfers",
                "Temporary employee management"
            ],
            prerequisites=[
                "HRIS system integration",
                "IT account management systems",
                "Learning management system (LMS)",
                "Document management platform"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Customize onboarding by department and role",
                "Add compliance training requirements",
                "Include equipment and access provisioning",
                "Set up manager and buddy assignments",
                "Configure progress tracking and reminders"
            ]
        )
    
    def _create_social_media_template(self) -> WorkflowTemplate:
        """Create social media management template."""
        
        variables = {
            "content_calendar": WorkflowVariable(
                name="content_calendar",
                value={},
                type="object",
                description="Social media content calendar"
            ),
            "platforms": WorkflowVariable(
                name="platforms",
                value=["twitter", "linkedin", "facebook", "instagram"],
                type="array",
                description="Target social media platforms"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="social_media_v1",
            name="Social Media Automation",
            description="Automated social media posting, engagement tracking, and content optimization",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "marketing"}
        )
        
        return WorkflowTemplate(
            id="social_media",
            name="Social Media Management Automation",
            description="Complete social media automation with content scheduling, engagement tracking, and performance analytics",
            category="Digital Marketing",
            difficulty="beginner",
            estimated_time="15-25 minutes setup",
            use_cases=[
                "Content calendar automation",
                "Cross-platform posting",
                "Engagement monitoring",
                "Influencer outreach"
            ],
            prerequisites=[
                "Social media platform APIs",
                "Content management system",
                "Analytics tracking tools",
                "Image and video assets"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Customize posting schedules by platform",
                "Add hashtag optimization",
                "Include content performance tracking",
                "Set up automated responses",
                "Configure crisis management protocols"
            ]
        )
    
    def _create_ecommerce_template(self) -> WorkflowTemplate:
        """Create e-commerce order processing template."""
        
        variables = {
            "order_data": WorkflowVariable(
                name="order_data",
                value={},
                type="object",
                description="Order information from e-commerce platform"
            ),
            "inventory_threshold": WorkflowVariable(
                name="inventory_threshold",
                value=10,
                type="number",
                description="Low inventory alert threshold"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="ecommerce_orders_v1",
            name="E-commerce Order Processing",
            description="Automated order processing with inventory management, shipping, and customer communication",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "ecommerce"}
        )
        
        return WorkflowTemplate(
            id="ecommerce_orders",
            name="E-commerce Order Processing",
            description="End-to-end order processing automation with inventory tracking, shipping integration, and customer updates",
            category="E-commerce",
            difficulty="intermediate",
            estimated_time="25-35 minutes setup",
            use_cases=[
                "Order fulfillment automation",
                "Inventory management",
                "Shipping and tracking",
                "Customer communication"
            ],
            prerequisites=[
                "E-commerce platform API (Shopify, WooCommerce, Magento)",
                "Inventory management system",
                "Shipping provider integrations",
                "Email notification system"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Configure different workflows by product type",
                "Add fraud detection and verification",
                "Include upselling and cross-selling",
                "Set up return and refund automation",
                "Add customer satisfaction surveys"
            ]
        )
    
    def _create_support_ticket_template(self) -> WorkflowTemplate:
        """Create support ticket management template."""
        
        variables = {
            "ticket_data": WorkflowVariable(
                name="ticket_data",
                value={},
                type="object",
                description="Support ticket information"
            ),
            "sla_hours": WorkflowVariable(
                name="sla_hours",
                value={"low": 72, "medium": 24, "high": 4, "critical": 1},
                type="object",
                description="SLA response times by priority"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="support_tickets_v1",
            name="Support Ticket Management",
            description="Intelligent support ticket routing, prioritization, and SLA management",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "support"}
        )
        
        return WorkflowTemplate(
            id="support_tickets",
            name="Intelligent Support Ticket Management",
            description="AI-powered ticket routing, priority classification, and automated resolution with SLA tracking",
            category="Customer Support",
            difficulty="intermediate",
            estimated_time="20-30 minutes setup",
            use_cases=[
                "Help desk automation",
                "Ticket routing and assignment",
                "SLA monitoring and alerts",
                "Customer satisfaction tracking"
            ],
            prerequisites=[
                "Help desk system (Zendesk, Freshdesk, ServiceNow)",
                "Knowledge base integration",
                "Team assignment rules",
                "Customer communication channels"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Train AI on historical ticket data",
                "Set up escalation rules and notifications",
                "Configure automated responses for common issues",
                "Add customer satisfaction surveys",
                "Include performance dashboards for agents"
            ]
        )
    
    def _create_content_creation_template(self) -> WorkflowTemplate:
        """Create content creation pipeline template."""
        
        variables = {
            "content_brief": WorkflowVariable(
                name="content_brief",
                value={},
                type="object",
                description="Content brief and requirements"
            ),
            "target_audience": WorkflowVariable(
                name="target_audience",
                value="",
                type="string",
                description="Target audience for content"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="content_creation_v1",
            name="AI-Powered Content Creation",
            description="Automated content creation pipeline with AI assistance, review workflows, and publishing",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "content"}
        )
        
        return WorkflowTemplate(
            id="content_creation",
            name="AI-Powered Content Creation Pipeline",
            description="Complete content creation workflow with AI assistance, collaborative editing, and multi-channel publishing",
            category="Content Marketing",
            difficulty="advanced",
            estimated_time="35-45 minutes setup",
            use_cases=[
                "Blog post creation",
                "Social media content",
                "Email newsletter automation",
                "Video script generation"
            ],
            prerequisites=[
                "Content management system",
                "AI writing tools integration",
                "Design and media assets",
                "Publishing platform APIs"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Configure AI prompts for your brand voice",
                "Set up approval workflows by content type",
                "Add SEO optimization steps",
                "Include plagiarism and fact-checking",
                "Configure multi-channel publishing schedules"
            ]
        )
    
    def _create_financial_reporting_template(self) -> WorkflowTemplate:
        """Create automated financial reporting template."""
        
        variables = {
            "report_period": WorkflowVariable(
                name="report_period",
                value="monthly",
                type="string",
                description="Reporting period (daily, weekly, monthly, quarterly)"
            ),
            "data_sources": WorkflowVariable(
                name="data_sources",
                value=[],
                type="array",
                description="Financial data sources and connections"
            )
        }
        
        workflow_def = WorkflowDefinition(
            id="financial_reporting_v1",
            name="Automated Financial Reporting",
            description="Comprehensive financial reporting with data consolidation, analysis, and distribution",
            version="1.0.0",
            nodes=[],
            edges=[],
            variables=variables,
            settings={"template": True, "category": "finance"}
        )
        
        return WorkflowTemplate(
            id="financial_reporting",
            name="Automated Financial Reporting",
            description="Comprehensive financial reporting automation with data consolidation, variance analysis, and stakeholder distribution",
            category="Finance & Accounting",
            difficulty="advanced",
            estimated_time="45-60 minutes setup",
            use_cases=[
                "Monthly financial reports",
                "KPI dashboards",
                "Budget vs actual analysis",
                "Executive reporting"
            ],
            prerequisites=[
                "Accounting system access",
                "Data warehouse or BI tools",
                "Report template designs",
                "Stakeholder distribution lists"
            ],
            workflow_definition=workflow_def,
            customization_tips=[
                "Configure automated data validation",
                "Set up variance analysis thresholds",
                "Add predictive analytics and forecasting",
                "Include compliance and audit trails",
                "Configure executive summary generation"
            ]
        )
    
    def get_template(self, template_id: str) -> WorkflowTemplate:
        """Get a specific workflow template."""
        return self.templates.get(template_id)
    
    def get_templates_by_category(self, category: str) -> List[WorkflowTemplate]:
        """Get all templates in a specific category."""
        return [
            template for template in self.templates.values()
            if template.category.lower() == category.lower()
        ]
    
    def get_templates_by_difficulty(self, difficulty: str) -> List[WorkflowTemplate]:
        """Get all templates by difficulty level."""
        return [
            template for template in self.templates.values()
            if template.difficulty.lower() == difficulty.lower()
        ]
    
    def search_templates(self, query: str) -> List[WorkflowTemplate]:
        """Search templates by name, description, or use cases."""
        query_lower = query.lower()
        results = []
        
        for template in self.templates.values():
            # Search in name and description
            if (query_lower in template.name.lower() or 
                query_lower in template.description.lower()):
                results.append(template)
                continue
            
            # Search in use cases
            for use_case in template.use_cases:
                if query_lower in use_case.lower():
                    results.append(template)
                    break
        
        return results
    
    def get_all_templates(self) -> List[WorkflowTemplate]:
        """Get all available templates."""
        return list(self.templates.values())
    
    def get_template_categories(self) -> List[str]:
        """Get all available template categories."""
        categories = set()
        for template in self.templates.values():
            categories.add(template.category)
        return sorted(list(categories))


# Global template library instance
template_library = EliteTemplateLibrary()