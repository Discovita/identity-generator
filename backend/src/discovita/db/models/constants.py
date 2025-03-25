"""Constants for database models."""

# Common column names
ID = "id"
USER_ID = "user_id"
SESSION_ID = "session_id"
CREATED_AT = "created_at"
UPDATED_AT = "updated_at"

# State columns
STATE_DATA = "state_data"

# Context columns
MESSAGES = "messages"
USER_DATA = "user_data"

# Identity columns
NAME = "name"
CATEGORY = "category"
DESCRIPTION = "description"

# Table names
STATES_TABLE = "states"
CONTEXTS_TABLE = "contexts"
IDENTITIES_TABLE = "identities"
USERS_TABLE = "users"

# Relationship names
USER_STATES = "states"
USER_CONTEXTS = "contexts"
USER_IDENTITIES = "identities"
USER = "user"
