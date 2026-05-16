# Policy Engine

Actions are classified into:

- `safe_to_suggest`: informational or low-risk recommendations.
- `requires_human_review`: rollback, traffic shift, scaling, or config changes.
- `never_auto_execute`: destructive data operations or broad customer-impacting actions.

The bootstrap never executes actions. It returns policy decisions and approval requirements.

