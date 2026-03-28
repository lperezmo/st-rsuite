"""Shared data constants for tree / cascade demos."""

TREE_DATA = [
    {
        "value": "root",
        "label": "Root",
        "children": [
            {
                "value": "frontend",
                "label": "Frontend",
                "children": [
                    {"value": "react", "label": "React"},
                    {"value": "vue", "label": "Vue"},
                    {"value": "angular", "label": "Angular"},
                ],
            },
            {
                "value": "backend",
                "label": "Backend",
                "children": [
                    {"value": "python", "label": "Python"},
                    {"value": "nodejs", "label": "Node.js"},
                    {"value": "go", "label": "Go"},
                ],
            },
            {
                "value": "database",
                "label": "Database",
                "children": [
                    {"value": "postgres", "label": "PostgreSQL"},
                    {"value": "mongodb", "label": "MongoDB"},
                    {"value": "redis", "label": "Redis"},
                ],
            },
        ],
    }
]

PICKER_DATA = [
    {
        "value": "engineering",
        "label": "Engineering",
        "children": [
            {
                "value": "frontend-team",
                "label": "Frontend Team",
                "children": [
                    {"value": "alice", "label": "Alice"},
                    {"value": "bob", "label": "Bob"},
                    {"value": "carol", "label": "Carol"},
                ],
            },
            {
                "value": "backend-team",
                "label": "Backend Team",
                "children": [
                    {"value": "dave", "label": "Dave"},
                    {"value": "eve", "label": "Eve"},
                ],
            },
        ],
    },
    {
        "value": "design",
        "label": "Design",
        "children": [
            {"value": "frank", "label": "Frank"},
            {"value": "grace", "label": "Grace"},
        ],
    },
    {
        "value": "product",
        "label": "Product",
        "children": [
            {"value": "heidi", "label": "Heidi"},
            {"value": "ivan", "label": "Ivan"},
        ],
    },
]

CASCADE_DATA = [
    {
        "value": "us",
        "label": "United States",
        "children": [
            {
                "value": "ca",
                "label": "California",
                "children": [
                    {"value": "sf", "label": "San Francisco"},
                    {"value": "la", "label": "Los Angeles"},
                    {"value": "sd", "label": "San Diego"},
                ],
            },
            {
                "value": "ny",
                "label": "New York",
                "children": [
                    {"value": "nyc", "label": "New York City"},
                    {"value": "buf", "label": "Buffalo"},
                ],
            },
            {
                "value": "tx",
                "label": "Texas",
                "children": [
                    {"value": "hou", "label": "Houston"},
                    {"value": "dal", "label": "Dallas"},
                    {"value": "aus", "label": "Austin"},
                ],
            },
        ],
    },
    {
        "value": "uk",
        "label": "United Kingdom",
        "children": [
            {
                "value": "eng",
                "label": "England",
                "children": [
                    {"value": "lon", "label": "London"},
                    {"value": "man", "label": "Manchester"},
                ],
            },
            {
                "value": "sco",
                "label": "Scotland",
                "children": [
                    {"value": "edi", "label": "Edinburgh"},
                    {"value": "gla", "label": "Glasgow"},
                ],
            },
        ],
    },
]
