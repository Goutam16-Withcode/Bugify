from agents.fix.subagents.patch_generator import PatchGenerator
g = PatchGenerator()
p = g._build_prompt(
    problem='Fix NoneType in user_service.py',
    traceback='File "app/user_service.py", line 2, in get_user_profile\n    profile = user_repo.find_by_id(user_id).get_data()\nAttributeError: NoneType object has no attribute get_data',
    root_cause='user evaluated to None',
    relevant_files=['app/user_service.py'],
    code_context={'app/user_service.py': {'source': 'def get_user_profile(user_id):\n    profile = user_repo.find_by_id(user_id).get_data()\n    return profile'}},
    retrieved_context=[]
)
resp = g.llm.invoke(p)
print("RESPONSE CONTENT:\n", resp.content)
patch = g._extract_patch(resp.content)
print("EXTRACTED PATCH:\n", patch)
