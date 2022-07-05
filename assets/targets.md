## Makefile Targets
-e The following targets are available: 

```
debug/incident                 Run the Lambda IR function
delete                         Delete application
dependencies                   Add Python dependencies
deploy/custom                  Deploy the SAM app with custom params
deploy/guided                  Guided deployment
deploy                         Deploy the SAM app (once deploy/guided has been runn to generate a samconfig.yaml)
package                        Create CF output
```
