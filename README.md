# daily_fudan_actions
daily_fudan的运行器，自动定时执行https://github.com/Limour-dev/daily_fudan_core 的代码
# GitHub CI 60 days limit
https://docs.github.com/cn/actions/managing-workflow-runs/disabling-and-enabling-a-workflow  
为防止不必要的工作流程运行，可能会自动禁用计划的工作流程。 在复刻公共仓库时，默认情况下将禁用计划的工作流程。 在公共仓库中，当 60 天内未发生仓库活动时，将自动禁用计划的工作流程。  

可能的解决方案：https://github.com/Limour-dev/secret_actions/wiki#actions-secrets  
申请无限期有修改权限的token，新建名为"GH_PAT"的Actions secrets，将token填入其中。
