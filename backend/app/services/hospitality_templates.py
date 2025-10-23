"""
Hospitality Workflow Templates
Based on survey feedback analysis - addresses specific pain points identified:

Survey Findings Summary:
- 100% experience communication delays between departments  
- 79% need multilingual support
- 64% need accessibility features  
- 50% report tasks get missed/duplicated "sometimes"
- 86% want tools that are easy, time-saving, mobile-friendly with management support
- 40% report no system for tracking guest service requests
- 40% have no alerts/reminders for time-sensitive tasks

Key Pain Points Addressed:
1. "Sometimes I feel like I'm playing detective just to figure out what happened on the last shift"
2. "No centralized task board or live status updates"
3. "Communication gaps between departments" 
4. "Tasks not being completed or followed up on"
5. "No alerts or reminders for time-sensitive tasks"
6. "Manual processes that could be automated"
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

class WorkflowTemplate:
    """Template for common hospitality workflows"""
    
    def __init__(self, name: str, description: str, departments: List[str], 
                 estimated_duration: int, priority: str = "medium"):
        self.name = name
        self.description = description
        self.departments = departments
        self.estimated_duration = estimated_duration
        self.priority = priority
        self.steps = []
        self.triggers = []
        self.automations = []

# Template 1: Guest Checkout Workflow
# Addresses: "Process checkout for Smith family, check for damages"
guest_checkout_template = {
    "name": "Guest Checkout Process",
    "description": "Complete guest checkout with cross-department coordination",
    "departments": ["front_desk", "housekeeping", "maintenance", "management"],
    "estimated_duration": 30,
    "priority": "high",
    "trigger": {
        "type": "guest_checkout_request",
        "conditions": ["guest_ready_to_checkout", "room_number_provided"]
    },
    "steps": [
        {
            "id": "checkout_001",
            "name": "Process Payment & Final Bill",
            "department": "front_desk",
            "duration": 8,
            "description": "Process final payment, print receipt, handle any disputes",
            "required_fields": ["final_bill_amount", "payment_method", "receipt_number"],
            "automations": [
                "auto_calculate_final_bill",
                "send_receipt_email",
                "update_guest_profile"
            ],
            "multilingual_support": {
                "en": "Process payment and print receipt",
                "es": "Procesar pago e imprimir recibo", 
                "fr": "Traiter le paiement et imprimer le reçu"
            }
        },
        {
            "id": "checkout_002", 
            "name": "Guest Satisfaction Survey",
            "department": "front_desk",
            "duration": 5,
            "description": "Collect guest feedback via mobile survey or verbal feedback",
            "required_fields": ["satisfaction_score", "feedback_comments"],
            "automations": [
                "send_mobile_survey_link",
                "auto_record_feedback",
                "trigger_service_recovery_if_needed"
            ],
            "accessibility_features": {
                "large_text": True,
                "audio_survey": True,
                "multilingual": True
            }
        },
        {
            "id": "checkout_003",
            "name": "Room Inspection Alert",
            "department": "housekeeping", 
            "duration": 2,
            "description": "Immediate alert to housekeeping for room inspection",
            "auto_trigger": True,
            "alert_escalation": {
                "initial": 0,      # Immediate
                "first_reminder": 5,   # 5 minutes
                "escalate_to_supervisor": 15  # 15 minutes
            },
            "required_actions": ["acknowledge_alert", "estimated_inspection_time"],
            "communication": {
                "quick_responses": [
                    "heading_to_room_now",
                    "delayed_5_minutes", 
                    "need_assistance",
                    "guest_still_in_room"
                ]
            }
        },
        {
            "id": "checkout_004",
            "name": "Room Status Update",
            "department": "housekeeping",
            "duration": 15,
            "description": "Inspect room, note any damages or maintenance needs",
            "required_fields": ["room_condition", "damages_found", "maintenance_required"],
            "voice_input_enabled": True,
            "automations": [
                "auto_photo_damage_detection",
                "create_maintenance_tickets",
                "update_room_status_system"
            ],
            "escalation_triggers": [
                "significant_damage_found",
                "maintenance_required",
                "unusual_conditions"
            ]
        },
        {
            "id": "checkout_005",
            "name": "Maintenance Review",
            "department": "maintenance",
            "duration": 0,
            "description": "Review maintenance requests from room inspection",
            "conditional": "maintenance_required == true",
            "auto_assign": True,
            "priority_escalation": {
                "guest_impact": "urgent",
                "safety_concern": "urgent", 
                "cosmetic_only": "medium"
            }
        },
        {
            "id": "checkout_006",
            "name": "Room Ready for Sale",
            "department": "housekeeping",
            "duration": 0,
            "description": "Mark room as clean and ready for next guest",
            "conditions": ["room_cleaned", "maintenance_complete", "inspection_passed"],
            "automations": [
                "update_property_management_system",
                "notify_front_desk_availability",
                "update_housekeeping_dashboard"
            ],
            "completion_notification": {
                "departments": ["front_desk", "management"],
                "message_templates": {
                    "en": "Room {room_number} ready for sale - checkout complete",
                    "es": "Habitación {room_number} lista para venta - checkout completo",
                    "fr": "Chambre {room_number} prête à la vente - checkout terminé"
                }
            }
        }
    ],
    "success_metrics": {
        "target_completion_time": 30,
        "guest_satisfaction_threshold": 4.0,
        "communication_response_time": 5
    },
    "escalation_rules": {
        "total_time_exceeded": "notify_management",
        "guest_complaint": "immediate_supervisor_involvement",
        "damage_discovered": "security_and_management_alert"
    }
}

# Template 2: Maintenance Request Workflow  
# Addresses: "Guest reports AC making loud noise, investigate and repair"
maintenance_request_template = {
    "name": "Maintenance Request - Guest Issue",
    "description": "Handle guest-reported maintenance issues with real-time updates",
    "departments": ["front_desk", "maintenance", "housekeeping", "management"],
    "estimated_duration": 45,
    "priority": "high",
    "trigger": {
        "type": "guest_maintenance_complaint",
        "urgency_detection": True,
        "auto_categorization": True
    },
    "steps": [
        {
            "id": "maint_001",
            "name": "Log Guest Complaint",
            "department": "front_desk", 
            "duration": 3,
            "description": "Record detailed complaint information with guest contact",
            "required_fields": [
                "guest_name", "room_number", "issue_description",
                "urgency_level", "guest_contact_preference"
            ],
            "automations": [
                "auto_detect_issue_category",
                "suggest_urgency_level",
                "create_ticket_number"
            ],
            "immediate_actions": [
                "send_acknowledgment_to_guest",
                "alert_maintenance_team",
                "start_response_timer"
            ]
        },
        {
            "id": "maint_002",
            "name": "Maintenance Team Response",
            "department": "maintenance",
            "duration": 2,
            "description": "Acknowledge request and provide estimated response time",
            "alert_escalation": {
                "urgent_issues": 2,     # 2 minutes
                "high_priority": 5,     # 5 minutes  
                "medium_priority": 10   # 10 minutes
            },
            "required_actions": [
                "acknowledge_request",
                "provide_eta",
                "request_additional_info_if_needed"
            ],
            "auto_responses": {
                "immediate_ack": "Maintenance request received - technician dispatched",
                "delay_notification": "Technician delayed - new ETA provided"
            }
        },
        {
            "id": "maint_003",
            "name": "Guest Notification",
            "department": "front_desk",
            "duration": 1,
            "description": "Update guest on technician dispatch and expected arrival",
            "automations": [
                "auto_call_or_text_guest",
                "provide_ticket_number",
                "set_guest_expectations"
            ],
            "multilingual_templates": {
                "en": "Maintenance technician en route to room {room} - ETA {eta}",
                "es": "Técnico de mantenimiento en camino a habitación {room} - ETA {eta}",
                "fr": "Technicien de maintenance en route vers chambre {room} - ETA {eta}"
            }
        },
        {
            "id": "maint_004",
            "name": "On-Site Assessment",
            "department": "maintenance", 
            "duration": 15,
            "description": "Assess issue, determine repair requirements, provide update",
            "location_tracking": True,
            "voice_updates_enabled": True,
            "required_actions": [
                "check_in_at_room",
                "assess_problem", 
                "determine_repair_approach",
                "update_all_parties"
            ],
            "escalation_conditions": [
                "requires_specialist",
                "safety_concern_identified",
                "cannot_repair_immediately",
                "guest_accommodation_needed"
            ]
        },
        {
            "id": "maint_005",
            "name": "Repair Execution",
            "department": "maintenance",
            "duration": 25,
            "description": "Complete repair work with real-time progress updates",
            "progress_tracking": True,
            "guest_communication": {
                "progress_updates": [15, 30],  # Update guest at 15 and 30 minutes
                "completion_notification": True,
                "satisfaction_check": True
            },
            "parallel_tasks": {
                "if_guest_relocation_needed": {
                    "department": "front_desk",
                    "action": "arrange_temporary_accommodation",
                    "duration": 10
                },
                "if_housekeeping_needed": {
                    "department": "housekeeping", 
                    "action": "post_repair_cleaning",
                    "duration": 15
                }
            }
        },
        {
            "id": "maint_006",
            "name": "Quality Check & Guest Verification",
            "department": "maintenance",
            "duration": 5,
            "description": "Test repair, get guest approval, complete documentation",
            "required_verification": [
                "repair_function_test",
                "guest_satisfaction_check",
                "safety_verification"
            ],
            "completion_requirements": [
                "guest_signs_off",
                "photo_documentation",
                "update_maintenance_log"
            ]
        },
        {
            "id": "maint_007",
            "name": "Follow-up & Closure",
            "department": "front_desk",
            "duration": 2,
            "description": "Ensure guest satisfaction and close ticket",
            "follow_up_schedule": {
                "immediate": "post_repair_satisfaction",
                "24_hours": "ensure_no_recurring_issues",
                "48_hours": "final_satisfaction_check"
            },
            "automations": [
                "send_satisfaction_survey",
                "update_guest_profile",
                "close_maintenance_ticket",
                "update_preventive_maintenance_schedule"
            ]
        }
    ],
    "real_time_tracking": {
        "guest_updates": [
            "technician_dispatched",
            "technician_arrived", 
            "assessment_complete",
            "repair_in_progress",
            "repair_completed",
            "quality_check_passed"
        ],
        "management_dashboard": [
            "response_time_tracking",
            "guest_satisfaction_monitoring",
            "technician_utilization",
            "issue_pattern_analysis"
        ]
    }
}

# Template 3: Event Setup Coordination
# Addresses: "Set up ballroom for 150 guests, coordinate with catering"
event_setup_template = {
    "name": "Banquet Event Setup",
    "description": "Multi-department coordination for event setup",
    "departments": ["banquet_events", "housekeeping", "maintenance", "bar_restaurant", "management"],
    "estimated_duration": 120,
    "priority": "high",
    "coordination_required": True,
    "steps": [
        {
            "id": "event_001",
            "name": "Pre-Setup Department Sync",
            "department": "banquet_events",
            "duration": 10,
            "description": "Coordinate with all departments for event requirements",
            "parallel_notifications": {
                "housekeeping": "Room cleaning and preparation requirements",
                "maintenance": "AV equipment and room setup needs",
                "bar_restaurant": "Catering coordination and timing",
                "management": "Special requirements and VIP considerations"
            },
            "coordination_meeting": {
                "virtual_check_in": True,
                "status_dashboard": True,
                "real_time_chat": True
            }
        },
        {
            "id": "event_002",
            "name": "Room Preparation",
            "department": "housekeeping",
            "duration": 30,
            "description": "Deep clean and prepare event space",
            "parallel_execution": True,
            "progress_tracking": {
                "checklist_items": [
                    "deep_clean_complete",
                    "carpet_vacuumed",
                    "windows_cleaned", 
                    "lighting_adjusted",
                    "temperature_set"
                ],
                "photo_documentation": True,
                "real_time_updates": True
            }
        },
        {
            "id": "event_003", 
            "name": "Technical Setup",
            "department": "maintenance",
            "duration": 45,
            "description": "Set up AV equipment, lighting, and technical requirements",
            "parallel_with": ["event_002"],
            "technical_checklist": [
                "sound_system_test",
                "microphone_setup",
                "projector_alignment",
                "lighting_programming",
                "backup_equipment_ready"
            ],
            "quality_assurance": {
                "sound_test_required": True,
                "visual_test_required": True,
                "backup_system_test": True
            }
        },
        {
            "id": "event_004",
            "name": "Furniture & Decor Setup", 
            "department": "banquet_events",
            "duration": 60,
            "description": "Arrange tables, chairs, decorations per event specifications",
            "dependencies": ["event_002", "event_003"],
            "setup_verification": {
                "table_count_verification": True,
                "seating_arrangement_check": True,
                "decoration_placement_approval": True,
                "client_walk_through": True
            }
        },
        {
            "id": "event_005",
            "name": "Catering Coordination",
            "department": "bar_restaurant", 
            "duration": 30,
            "description": "Set up catering stations and coordinate service timing",
            "parallel_with": ["event_004"],
            "coordination_points": [
                "kitchen_prep_timing",
                "service_station_setup",
                "staff_briefing_complete",
                "special_dietary_accommodations"
            ]
        },
        {
            "id": "event_006",
            "name": "Final Inspection & Sign-Off",
            "department": "management",
            "duration": 15,
            "description": "Final quality check and client approval",
            "dependencies": ["event_004", "event_005"],
            "inspection_criteria": [
                "all_departments_signed_off",
                "client_expectations_met",
                "safety_requirements_verified",
                "contingency_plans_in_place"
            ],
            "client_interaction": {
                "walk_through_required": True,
                "sign_off_documentation": True,
                "last_minute_adjustments": True
            }
        }
    ],
    "communication_protocols": {
        "real_time_chat": "All departments in event setup chat",
        "progress_dashboard": "Live progress visible to all teams",
        "escalation_path": "Event manager → Department heads → General manager",
        "client_updates": "Automated progress notifications to client"
    }
}

# Template 4: Shift Handoff Process
# Addresses: "Sometimes I feel like I'm playing detective just to figure out what happened on the last shift"
shift_handoff_template = {
    "name": "Comprehensive Shift Handoff",
    "description": "Structured information transfer between shifts",
    "departments": ["all"],
    "estimated_duration": 15,
    "priority": "critical",
    "automation_level": "high",
    "steps": [
        {
            "id": "handoff_001",
            "name": "Auto-Generate Shift Summary",
            "department": "system",
            "duration": 2,
            "description": "System compiles shift activity summary",
            "automations": [
                "compile_completed_tasks",
                "identify_pending_items",
                "flag_outstanding_issues",
                "generate_handoff_report",
                "identify_trends_and_patterns"
            ],
            "data_sources": [
                "task_completion_log",
                "guest_interactions",
                "maintenance_requests",
                "incident_reports",
                "inventory_updates"
            ]
        },
        {
            "id": "handoff_002",
            "name": "Department Status Reviews",
            "department": "all",
            "duration": 8,
            "description": "Each department reviews and adds context to auto-generated summary",
            "department_specific": {
                "front_desk": {
                    "key_items": [
                        "vip_guests_in_house",
                        "special_requests_pending",
                        "payment_issues",
                        "early_checkouts_tomorrow"
                    ]
                },
                "housekeeping": {
                    "key_items": [
                        "out_of_order_rooms",
                        "maintenance_requests_submitted",
                        "inventory_concerns",
                        "staffing_adjustments"
                    ]
                },
                "maintenance": {
                    "key_items": [
                        "urgent_repairs_pending",
                        "preventive_maintenance_scheduled",
                        "equipment_status_updates",
                        "safety_concerns"
                    ]
                }
            },
            "voice_input_enabled": True,
            "multilingual_support": True
        },
        {
            "id": "handoff_003",
            "name": "Cross-Department Alerts",
            "department": "system",
            "duration": 3,
            "description": "Identify and highlight cross-department dependencies",
            "smart_analysis": [
                "identify_coordination_needs",
                "flag_potential_conflicts",
                "highlight_guest_impact_items",
                "predict_next_shift_priorities"
            ],
            "alert_categories": [
                "immediate_attention_required",
                "guest_facing_deadlines",
                "interdepartment_coordination_needed",
                "resource_constraints"
            ]
        },
        {
            "id": "handoff_004",
            "name": "Incoming Shift Briefing",
            "department": "management",
            "duration": 2,
            "description": "Brief incoming shift on priorities and key issues",
            "delivery_methods": [
                "live_briefing_session",
                "recorded_video_summary",
                "interactive_dashboard_review",
                "mobile_app_notifications"
            ],
            "accessibility_options": {
                "audio_summary": True,
                "visual_dashboard": True,
                "text_summary": True,
                "multilingual_support": True
            }
        }
    ],
    "handoff_dashboard": {
        "sections": [
            "shift_highlights",
            "pending_guest_requests", 
            "maintenance_priorities",
            "staffing_notes",
            "special_events_tomorrow",
            "inventory_alerts",
            "safety_reminders"
        ],
        "real_time_updates": True,
        "mobile_optimized": True,
        "offline_access": True
    }
}

# Template 5: Guest Complaint Resolution
# Addresses: Service recovery and guest satisfaction tracking
guest_complaint_template = {
    "name": "Guest Complaint Resolution",
    "description": "Systematic approach to guest service recovery",
    "departments": ["front_desk", "management", "housekeeping", "maintenance"],
    "estimated_duration": 30,
    "priority": "urgent",
    "service_recovery": True,
    "steps": [
        {
            "id": "complaint_001",
            "name": "Immediate Guest Acknowledgment",
            "department": "front_desk",
            "duration": 2,
            "description": "Acknowledge complaint and show empathy",
            "response_time_target": 60,  # seconds
            "required_actions": [
                "listen_actively",
                "express_empathy",
                "apologize_for_inconvenience",
                "gather_initial_details"
            ],
            "escalation_triggers": [
                "guest_extremely_upset",
                "safety_concern_mentioned",
                "potential_legal_issue",
                "social_media_threat"
            ]
        },
        {
            "id": "complaint_002",
            "name": "Detailed Issue Documentation",
            "department": "front_desk",
            "duration": 5,
            "description": "Collect comprehensive complaint details",
            "documentation_requirements": [
                "guest_contact_information",
                "detailed_issue_description",
                "guest_desired_resolution",
                "timeline_of_events",
                "previous_interactions"
            ],
            "voice_recording_option": True,
            "photo_evidence_upload": True
        },
        {
            "id": "complaint_003",
            "name": "Management Notification & Response",
            "department": "management",
            "duration": 3,
            "description": "Manager reviews complaint and determines response strategy",
            "auto_escalation_criteria": [
                "guest_satisfaction_score_below_3",
                "repeat_complaint_from_guest",
                "high_value_guest",
                "potential_reputation_impact"
            ],
            "response_authorization": {
                "compensation_limits": "per_manager_level",
                "service_recovery_options": "pre_approved_list",
                "escalation_to_gm": "defined_criteria"
            }
        },
        {
            "id": "complaint_004",
            "name": "Service Recovery Implementation",
            "department": "front_desk",
            "duration": 15,
            "description": "Implement agreed resolution and follow up",
            "service_recovery_options": [
                "room_upgrade",
                "meal_vouchers",
                "late_checkout",
                "spa_credits",
                "partial_refund",
                "future_stay_discount"
            ],
            "implementation_tracking": True,
            "guest_approval_required": True
        },
        {
            "id": "complaint_005",
            "name": "Resolution Follow-up",
            "department": "management",
            "duration": 5,
            "description": "Ensure guest satisfaction and prevent recurrence",
            "follow_up_schedule": {
                "immediate": "resolution_satisfaction_check",
                "24_hours": "ensure_no_additional_issues",
                "post_checkout": "final_satisfaction_survey"
            },
            "learning_integration": [
                "identify_root_cause",
                "update_procedures_if_needed",
                "staff_training_recommendations",
                "system_improvements"
            ]
        }
    ],
    "guest_communication": {
        "acknowledgment_time": "60_seconds",
        "update_frequency": "every_15_minutes",
        "resolution_confirmation": "guest_sign_off_required",
        "satisfaction_measurement": "1_to_5_scale"
    }
}

# Master template registry
HOSPITALITY_TEMPLATES = {
    "guest_checkout": guest_checkout_template,
    "maintenance_request": maintenance_request_template, 
    "event_setup": event_setup_template,
    "shift_handoff": shift_handoff_template,
    "guest_complaint": guest_complaint_template
}

# Template deployment configurations based on survey feedback
DEPLOYMENT_CONFIG = {
    "mobile_optimization": {
        "touch_targets": "minimum_44px",
        "font_size": "minimum_16px", 
        "offline_mode": True,
        "push_notifications": True,
        "voice_input": True
    },
    "accessibility_requirements": {
        "large_text_support": True,
        "high_contrast_mode": True,
        "screen_reader_compatible": True,
        "voice_navigation": True,
        "simplified_ui_option": True
    },
    "multilingual_support": {
        "supported_languages": ["en", "es", "fr"],
        "auto_translation": True,
        "voice_recognition_multilingual": True,
        "cultural_date_time_formats": True
    },
    "communication_features": {
        "real_time_chat": True,
        "department_alerts": True,
        "escalation_automation": True,
        "quick_response_templates": True,
        "voice_to_text": True
    },
    "task_accountability": {
        "auto_escalation": True,
        "completion_tracking": True,
        "handoff_documentation": True,
        "performance_analytics": True,
        "guest_impact_flagging": True
    }
}

def get_template(template_name: str) -> Dict[str, Any]:
    """Get a specific workflow template"""
    return HOSPITALITY_TEMPLATES.get(template_name)

def get_all_templates() -> Dict[str, Dict[str, Any]]:
    """Get all available workflow templates"""
    return HOSPITALITY_TEMPLATES

def customize_template_for_property(template: Dict[str, Any], property_config: Dict[str, Any]) -> Dict[str, Any]:
    """Customize template based on specific property requirements"""
    # Implementation would modify template based on property size, type, etc.
    customized = template.copy()
    
    # Adjust timing based on property size
    if property_config.get("property_size") == "large":
        for step in customized.get("steps", []):
            step["duration"] = int(step["duration"] * 1.2)  # 20% more time for large properties
    
    return customized