---
title: "Spark Structured Streaming"
company: "databricks"
url: "https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html"
content_length: 45500
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

Skip to main content

[![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTMyIiBoZWlnaHQ9IjIyIiB2aWV3Qm94PSIwIDAgMTMyIDIyIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Im0xOC4zMTggOS4yNzUtOC42MzEgNC44NTlMLjQ0NSA4Ljk0MiAwIDkuMTgydjMuNzdsOS42ODcgNS40MzEgOC42My00Ljg0djEuOTk1bC04LjYzIDQuODYtOS4yNDItNS4xOTItLjQ0NS4yNHYuNjQ2bDkuNjg3IDUuNDMyIDkuNjY4LTUuNDMydi0zLjc2OWwtLjQ0NS0uMjQtOS4yMjMgNS4xNzMtOC42NS00Ljg0VjEwLjQybDguNjUgNC44NCA5LjY2OC01LjQzVjYuMTE0bC0uNDgyLS4yNzctOS4xODYgNS4xNTVMMS40ODIgNi40MWw4LjIwNS00LjYgNi43NDEgMy43ODcuNTkzLS4zMzJ2LS40NjJMOS42ODcuNjg0IDAgNi4xMTV2LjU5Mmw5LjY4NyA1LjQzMiA4LjYzLTQuODZ6IiBmaWxsPSIjRUUzRDJDIi8+PHBhdGggZD0iTTM3LjQ0OSAxOC40NDNWMS44NTJoLTIuNTU2djYuMjA3YzAgLjA5My0uMDU2LjE2Ny0uMTQ4LjIwNGEuMjMuMjMgMCAwIDEtLjI0LS4wNTZjLS44NzEtMS4wMTYtMi4yMjMtMS41ODktMy43MDUtMS41ODktMy4xNjcgMC01LjY1IDIuNjYtNS42NSA2LjA2IDAgMS42NjMuNTc1IDMuMTk3IDEuNjMgNC4zMjRhNS40NCA1LjQ0IDAgMCAwIDQuMDIgMS43MzZjMS40NjMgMCAyLjgxNS0uNjEgMy43MDQtMS42NjIuMDU2LS4wNzQuMTY3LS4wOTMuMjQtLjA3NC4wOTMuMDM3LjE1LjExLjE1LjIwM3YxLjIzOHptLTYuMDkzLTIuMDE0Yy0yLjAzOCAwLTMuNjMtMS42NDQtMy42My0zLjc1IDAtMi4xMDcgMS41OTItMy43NTEgMy42My0zLjc1MXMzLjYzIDEuNjQ0IDMuNjMgMy43NS0xLjU5MyAzLjc1LTMuNjMgMy43NW0xOS43NjIgMi4wMTZWNi44OTZoLTIuNTM3VjguMDZjMCAuMDkzLS4wNTYuMTY2LS4xNDkuMjAzYS4yLjIgMCAwIDEtLjI0LS4wNzNjLS44NTItMS4wMTctMi4xODYtMS41OS0zLjcwNS0xLjU5LTMuMTY3IDAtNS42NDkgMi42NjEtNS42NDkgNi4wNiAwIDMuNCAyLjQ4MiA2LjA2IDUuNjUgNi4wNiAxLjQ2MyAwIDIuODE1LS42MSAzLjcwNC0xLjY4LjA1NS0uMDc1LjE2Ni0uMDkzLjI0LS4wNzUuMDkzLjAzNy4xNDkuMTExLjE0OS4yMDR2MS4yNTZoMi41Mzd6bS02LjA1Ni0yLjAxNGMtMi4wMzggMC0zLjYzLTEuNjQ1LTMuNjMtMy43NSAwLTIuMTA3IDEuNTkyLTMuNzUxIDMuNjMtMy43NTFzMy42MyAxLjY0NCAzLjYzIDMuNzUtMS41OTMgMy43NS0zLjYzIDMuNzVtMjcuNzgxIDIuMDE1VjYuODk2aC0yLjUzOFY4LjA2YzAgLjA5My0uMDU1LjE2Ni0uMTQ4LjIwM3MtLjE4NSAwLS4yNC0uMDczYy0uODUzLTEuMDE3LTIuMTg2LTEuNTktMy43MDUtMS41OS0zLjE4NiAwLTUuNjQ5IDIuNjYxLTUuNjQ5IDYuMDggMCAzLjQxNyAyLjQ4MiA2LjA2IDUuNjQ5IDYuMDYgMS40NjMgMCAyLjgxNS0uNjEgMy43MDQtMS42ODIuMDU2LS4wNzQuMTY3LS4wOTMuMjQxLS4wNzQuMDkzLjAzNy4xNDguMTEuMTQ4LjIwM3YxLjI1NnptLTYuMDU3LTIuMDE0Yy0yLjAzNyAwLTMuNjMtMS42NDUtMy42My0zLjc1IDAtMi4xMDcgMS41OTMtMy43NTEgMy42My0zLjc1MXMzLjYzIDEuNjQ0IDMuNjMgMy43NS0xLjU5MyAzLjc1LTMuNjMgMy43NW0xMC43MDYuNjQ3Yy4wMTkgMCAuMDU2LS4wMTkuMDc0LS4wMTkuMDU2IDAgLjEzLjAzNy4xNjcuMDc0Ljg3IDEuMDE2IDIuMjIyIDEuNTg5IDMuNzA0IDEuNTg5IDMuMTY3IDAgNS42NS0yLjY2IDUuNjUtNi4wNiAwLTEuNjYzLS41NzUtMy4xOTYtMS42My00LjMyM2E1LjQ0IDUuNDQgMCAwIDAtNC4wMi0xLjczN2MtMS40NjMgMC0yLjgxNS42MS0zLjcwNCAxLjY2My0uMDU2LjA3NC0uMTQ4LjA5Mi0uMjQuMDc0LS4wOTMtLjAzNy0uMTQ5LS4xMTEtLjE0OS0uMjA0VjEuODUyaC0yLjU1NnYxNi41OWgyLjU1NlYxNy4yOGMwLS4wOTMuMDU2LS4xNjYuMTQ4LS4yMDNtLS4yNi00LjM5OGMwLTIuMTA2IDEuNTk0LTMuNzUgMy42MzEtMy43NXMzLjYzIDEuNjQ0IDMuNjMgMy43NS0xLjU5MyAzLjc1LTMuNjMgMy43NS0zLjYzLTEuNjYyLTMuNjMtMy43NW0xNy4yNDQtMy40MTZjLjI0IDAgLjQ2My4wMTkuNjEuMDU2VjYuNjk1YTIuNCAyLjQgMCAwIDAtLjQyNS0uMDM3Yy0xLjMzNCAwLTIuNTU2LjY4NC0zLjIwNCAxLjc3NC0uMDU2LjA5Mi0uMTQ5LjEzLS4yNDEuMDkyYS4yMi4yMiAwIDAgMS0uMTY3LS4yMDNWNi44OThoLTIuNTM3djExLjU2NmgyLjU1NnYtNS4xYzAtMi41MyAxLjI5Ni00LjEgMy40MDgtNC4xbTQuODE1LTIuMzY3aC0yLjU5M3YxMS41NjZoMi41OTN6TTk3Ljk1OCAxLjg3YTEuNTcxIDEuNTcxIDAgMSAwIDAgMy4xNDEgMS41NzEgMS41NzEgMCAxIDAgMC0zLjE0bTguOTI4IDQuNzI5Yy0zLjU1NiAwLTYuMTMxIDIuNTUtNi4xMzEgNi4wOCAwIDEuNzE3LjYxMiAzLjI1IDEuNzA0IDQuMzYgMS4xMTIgMS4xMDggMi42NjcgMS43MTggNC40MDggMS43MTggMS40NDUgMCAyLjU1Ni0uMjc3IDQuNjY4LTEuODNsLTEuNDYzLTEuNTMzYy0xLjAzOC42ODQtMi4wMDEgMS4wMTYtMi45NDUgMS4wMTYtMi4xNDkgMC0zLjc2LTEuNjA3LTMuNzYtMy43MzJzMS42MTEtMy43MzIgMy43Ni0zLjczMmMxLjAxOCAwIDEuOTYzLjMzMyAyLjkwOCAxLjAxNmwxLjYyOS0xLjUzM2MtMS45MDctMS42MjYtMy42My0xLjgzLTQuNzc4LTEuODNtOS4xNDkgNi43NjJhLjIuMiAwIDAgMSAuMTQ5LS4wNTVoLjAxOGMuMDU2IDAgLjExMS4wMzcuMTY3LjA3M2w0LjA5MyA1LjA2M2gzLjE0OWwtNS4yOTctNi4zOTNjLS4wNzUtLjA5Mi0uMDc1LS4yMjIuMDE4LS4yOTVsNC44NzEtNC44NmgtMy4xM2wtNC4yMDQgNC4yMTNjLS4wNTYuMDU1LS4xNDguMDc0LS4yNDEuMDU1YS4yMy4yMyAwIDAgMS0uMTMtLjIwM1YxLjg3aC0yLjU3NHYxNi41OTFoMi41NTZ2LTQuNTA4YzAtLjA1NS4wMTgtLjEzLjA3NC0uMTY2eiIgZmlsbD0iIzAwMCIvPjxwYXRoIGQ9Ik0xMjcuNzc2IDE4LjczOWMyLjA5MyAwIDQuMjIzLTEuMjc1IDQuMjIzLTMuNjk1IDAtMS41ODktMS0yLjY4LTMuMDM3LTMuMzQ0bC0xLjM5LS40NjJjLS45NDQtLjMxNC0xLjM4OS0uNzU4LTEuMzg5LTEuMzY3IDAtLjcwMi42My0xLjE4MyAxLjUxOS0xLjE4My44NTIgMCAxLjYxMS41NTUgMi4wOTMgMS41MTVsMi4wNTYtMS4xMDhjLS43NTktMS41NTItMi4zMzQtMi41MTMtNC4xNDktMi41MTMtMi4yOTcgMC0zLjk2MyAxLjQ3OC0zLjk2MyAzLjQ5MiAwIDEuNjA3Ljk2MyAyLjY3OSAyLjk0NCAzLjMwN2wxLjQyNy40NjJjMSAuMzE0IDEuNDI2LjcyIDEuNDI2IDEuMzY3IDAgLjk4LS45MDggMS4zMy0xLjY4NiAxLjMzLTEuMDM3IDAtMS45NjMtLjY2NS0yLjQwNy0xLjc1NWwtMi4wOTMgMS4xMDljLjY4NSAxLjc1NSAyLjM3IDIuODQ1IDQuNDI2IDIuODQ1bS02OS41NDYtLjExMWMuODE1IDAgMS41MzgtLjA3NCAxLjk0NS0uMTN2LTIuMjE2YTE0IDE0IDAgMCAxLTEuMjc4LjA3M2MtMS4wMzcgMC0xLjgzMy0uMTg0LTEuODMzLTIuNDJWOS4xODdjMC0uMTMuMDkyLS4yMjIuMjIyLS4yMjJoMi41VjYuODc3aC0yLjVhLjIxNC4yMTQgMCAwIDEtLjIyMi0uMjIxVjMuMzNoLTIuNTU2djMuMzQ0YzAgLjEzLS4wOTMuMjIyLS4yMjMuMjIyaC0xLjc3OHYyLjA4OGgxLjc3OGMuMTMgMCAuMjIzLjA5Mi4yMjMuMjIxdjUuMzc3YzAgNC4wNDYgMi43MDQgNC4wNDYgMy43MjIgNC4wNDYiIGZpbGw9IiMwMDAiLz48L3N2Zz4=)](/)

[Login](https://login.databricks.com/?dbx_source=www&itm=main-cta-login&l=en-EN)

[![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTMyIiBoZWlnaHQ9IjIyIiB2aWV3Qm94PSIwIDAgMTMyIDIyIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Im0xOC4zMTggOS4yNzUtOC42MzEgNC44NTlMLjQ0NSA4Ljk0MiAwIDkuMTgydjMuNzdsOS42ODcgNS40MzEgOC42My00Ljg0djEuOTk1bC04LjYzIDQuODYtOS4yNDItNS4xOTItLjQ0NS4yNHYuNjQ2bDkuNjg3IDUuNDMyIDkuNjY4LTUuNDMydi0zLjc2OWwtLjQ0NS0uMjQtOS4yMjMgNS4xNzMtOC42NS00Ljg0VjEwLjQybDguNjUgNC44NCA5LjY2OC01LjQzVjYuMTE0bC0uNDgyLS4yNzctOS4xODYgNS4xNTVMMS40ODIgNi40MWw4LjIwNS00LjYgNi43NDEgMy43ODcuNTkzLS4zMzJ2LS40NjJMOS42ODcuNjg0IDAgNi4xMTV2LjU5Mmw5LjY4NyA1LjQzMiA4LjYzLTQuODZ6IiBmaWxsPSIjRUUzRDJDIi8+PHBhdGggZD0iTTM3LjQ0OSAxOC40NDNWMS44NTJoLTIuNTU2djYuMjA3YzAgLjA5My0uMDU2LjE2Ny0uMTQ4LjIwNGEuMjMuMjMgMCAwIDEtLjI0LS4wNTZjLS44NzEtMS4wMTYtMi4yMjMtMS41ODktMy43MDUtMS41ODktMy4xNjcgMC01LjY1IDIuNjYtNS42NSA2LjA2IDAgMS42NjMuNTc1IDMuMTk3IDEuNjMgNC4zMjRhNS40NCA1LjQ0IDAgMCAwIDQuMDIgMS43MzZjMS40NjMgMCAyLjgxNS0uNjEgMy43MDQtMS42NjIuMDU2LS4wNzQuMTY3LS4wOTMuMjQtLjA3NC4wOTMuMDM3LjE1LjExLjE1LjIwM3YxLjIzOHptLTYuMDkzLTIuMDE0Yy0yLjAzOCAwLTMuNjMtMS42NDQtMy42My0zLjc1IDAtMi4xMDcgMS41OTItMy43NTEgMy42My0zLjc1MXMzLjYzIDEuNjQ0IDMuNjMgMy43NS0xLjU5MyAzLjc1LTMuNjMgMy43NW0xOS43NjIgMi4wMTZWNi44OTZoLTIuNTM3VjguMDZjMCAuMDkzLS4wNTYuMTY2LS4xNDkuMjAzYS4yLjIgMCAwIDEtLjI0LS4wNzNjLS44NTItMS4wMTctMi4xODYtMS41OS0zLjcwNS0xLjU5LTMuMTY3IDAtNS42NDkgMi42NjEtNS42NDkgNi4wNiAwIDMuNCAyLjQ4MiA2LjA2IDUuNjUgNi4wNiAxLjQ2MyAwIDIuODE1LS42MSAzLjcwNC0xLjY4LjA1NS0uMDc1LjE2Ni0uMDkzLjI0LS4wNzUuMDkzLjAzNy4xNDkuMTExLjE0OS4yMDR2MS4yNTZoMi41Mzd6bS02LjA1Ni0yLjAxNGMtMi4wMzggMC0zLjYzLTEuNjQ1LTMuNjMtMy43NSAwLTIuMTA3IDEuNTkyLTMuNzUxIDMuNjMtMy43NTFzMy42MyAxLjY0NCAzLjYzIDMuNzUtMS41OTMgMy43NS0zLjYzIDMuNzVtMjcuNzgxIDIuMDE1VjYuODk2aC0yLjUzOFY4LjA2YzAgLjA5My0uMDU1LjE2Ni0uMTQ4LjIwM3MtLjE4NSAwLS4yNC0uMDczYy0uODUzLTEuMDE3LTIuMTg2LTEuNTktMy43MDUtMS41OS0zLjE4NiAwLTUuNjQ5IDIuNjYxLTUuNjQ5IDYuMDggMCAzLjQxNyAyLjQ4MiA2LjA2IDUuNjQ5IDYuMDYgMS40NjMgMCAyLjgxNS0uNjEgMy43MDQtMS42ODIuMDU2LS4wNzQuMTY3LS4wOTMuMjQxLS4wNzQuMDkzLjAzNy4xNDguMTEuMTQ4LjIwM3YxLjI1NnptLTYuMDU3LTIuMDE0Yy0yLjAzNyAwLTMuNjMtMS42NDUtMy42My0zLjc1IDAtMi4xMDcgMS41OTMtMy43NTEgMy42My0zLjc1MXMzLjYzIDEuNjQ0IDMuNjMgMy43NS0xLjU5MyAzLjc1LTMuNjMgMy43NW0xMC43MDYuNjQ3Yy4wMTkgMCAuMDU2LS4wMTkuMDc0LS4wMTkuMDU2IDAgLjEzLjAzNy4xNjcuMDc0Ljg3IDEuMDE2IDIuMjIyIDEuNTg5IDMuNzA0IDEuNTg5IDMuMTY3IDAgNS42NS0yLjY2IDUuNjUtNi4wNiAwLTEuNjYzLS41NzUtMy4xOTYtMS42My00LjMyM2E1LjQ0IDUuNDQgMCAwIDAtNC4wMi0xLjczN2MtMS40NjMgMC0yLjgxNS42MS0zLjcwNCAxLjY2My0uMDU2LjA3NC0uMTQ4LjA5Mi0uMjQuMDc0LS4wOTMtLjAzNy0uMTQ5LS4xMTEtLjE0OS0uMjA0VjEuODUyaC0yLjU1NnYxNi41OWgyLjU1NlYxNy4yOGMwLS4wOTMuMDU2LS4xNjYuMTQ4LS4yMDNtLS4yNi00LjM5OGMwLTIuMTA2IDEuNTk0LTMuNzUgMy42MzEtMy43NXMzLjYzIDEuNjQ0IDMuNjMgMy43NS0xLjU5MyAzLjc1LTMuNjMgMy43NS0zLjYzLTEuNjYyLTMuNjMtMy43NW0xNy4yNDQtMy40MTZjLjI0IDAgLjQ2My4wMTkuNjEuMDU2VjYuNjk1YTIuNCAyLjQgMCAwIDAtLjQyNS0uMDM3Yy0xLjMzNCAwLTIuNTU2LjY4NC0zLjIwNCAxLjc3NC0uMDU2LjA5Mi0uMTQ5LjEzLS4yNDEuMDkyYS4yMi4yMiAwIDAgMS0uMTY3LS4yMDNWNi44OThoLTIuNTM3djExLjU2NmgyLjU1NnYtNS4xYzAtMi41MyAxLjI5Ni00LjEgMy40MDgtNC4xbTQuODE1LTIuMzY3aC0yLjU5M3YxMS41NjZoMi41OTN6TTk3Ljk1OCAxLjg3YTEuNTcxIDEuNTcxIDAgMSAwIDAgMy4xNDEgMS41NzEgMS41NzEgMCAxIDAgMC0zLjE0bTguOTI4IDQuNzI5Yy0zLjU1NiAwLTYuMTMxIDIuNTUtNi4xMzEgNi4wOCAwIDEuNzE3LjYxMiAzLjI1IDEuNzA0IDQuMzYgMS4xMTIgMS4xMDggMi42NjcgMS43MTggNC40MDggMS43MTggMS40NDUgMCAyLjU1Ni0uMjc3IDQuNjY4LTEuODNsLTEuNDYzLTEuNTMzYy0xLjAzOC42ODQtMi4wMDEgMS4wMTYtMi45NDUgMS4wMTYtMi4xNDkgMC0zLjc2LTEuNjA3LTMuNzYtMy43MzJzMS42MTEtMy43MzIgMy43Ni0zLjczMmMxLjAxOCAwIDEuOTYzLjMzMyAyLjkwOCAxLjAxNmwxLjYyOS0xLjUzM2MtMS45MDctMS42MjYtMy42My0xLjgzLTQuNzc4LTEuODNtOS4xNDkgNi43NjJhLjIuMiAwIDAgMSAuMTQ5LS4wNTVoLjAxOGMuMDU2IDAgLjExMS4wMzcuMTY3LjA3M2w0LjA5MyA1LjA2M2gzLjE0OWwtNS4yOTctNi4zOTNjLS4wNzUtLjA5Mi0uMDc1LS4yMjIuMDE4LS4yOTVsNC44NzEtNC44NmgtMy4xM2wtNC4yMDQgNC4yMTNjLS4wNTYuMDU1LS4xNDguMDc0LS4yNDEuMDU1YS4yMy4yMyAwIDAgMS0uMTMtLjIwM1YxLjg3aC0yLjU3NHYxNi41OTFoMi41NTZ2LTQuNTA4YzAtLjA1NS4wMTgtLjEzLjA3NC0uMTY2eiIgZmlsbD0iIzAwMCIvPjxwYXRoIGQ9Ik0xMjcuNzc2IDE4LjczOWMyLjA5MyAwIDQuMjIzLTEuMjc1IDQuMjIzLTMuNjk1IDAtMS41ODktMS0yLjY4LTMuMDM3LTMuMzQ0bC0xLjM5LS40NjJjLS45NDQtLjMxNC0xLjM4OS0uNzU4LTEuMzg5LTEuMzY3IDAtLjcwMi42My0xLjE4MyAxLjUxOS0xLjE4My44NTIgMCAxLjYxMS41NTUgMi4wOTMgMS41MTVsMi4wNTYtMS4xMDhjLS43NTktMS41NTItMi4zMzQtMi41MTMtNC4xNDktMi41MTMtMi4yOTcgMC0zLjk2MyAxLjQ3OC0zLjk2MyAzLjQ5MiAwIDEuNjA3Ljk2MyAyLjY3OSAyLjk0NCAzLjMwN2wxLjQyNy40NjJjMSAuMzE0IDEuNDI2LjcyIDEuNDI2IDEuMzY3IDAgLjk4LS45MDggMS4zMy0xLjY4NiAxLjMzLTEuMDM3IDAtMS45NjMtLjY2NS0yLjQwNy0xLjc1NWwtMi4wOTMgMS4xMDljLjY4NSAxLjc1NSAyLjM3IDIuODQ1IDQuNDI2IDIuODQ1bS02OS41NDYtLjExMWMuODE1IDAgMS41MzgtLjA3NCAxLjk0NS0uMTN2LTIuMjE2YTE0IDE0IDAgMCAxLTEuMjc4LjA3M2MtMS4wMzcgMC0xLjgzMy0uMTg0LTEuODMzLTIuNDJWOS4xODdjMC0uMTMuMDkyLS4yMjIuMjIyLS4yMjJoMi41VjYuODc3aC0yLjVhLjIxNC4yMTQgMCAwIDEtLjIyMi0uMjIxVjMuMzNoLTIuNTU2djMuMzQ0YzAgLjEzLS4wOTMuMjIyLS4yMjMuMjIyaC0xLjc3OHYyLjA4OGgxLjc3OGMuMTMgMCAuMjIzLjA5Mi4yMjMuMjIxdjUuMzc3YzAgNC4wNDYgMi43MDQgNC4wNDYgMy43MjIgNC4wNDYiIGZpbGw9IiMwMDAiLz48L3N2Zz4=)](/)

  * Why Databricks

    *       * Discover

        * [For Executives](/why-databricks/executives)
        * [For Startups ](/product/startups)
        * [Lakehouse Architecture ](/product/data-lakehouse)
        * [Mosaic Research](/research/mosaic)

      * Customers

        * [Customer Stories](/customers)

      * Partners

        * [Cloud ProvidersDatabricks on AWS, Azure, GCP, and SAP](/company/partners/cloud-partners)
        * [Consulting & System IntegratorsExperts to build, deploy and migrate to Databricks](/company/partners/consulting-and-si)
        * [Technology PartnersConnect your existing tools to your Lakehouse](/company/partners/technology-partner-program)
        * [C&SI Partner ProgramBuild, deploy or migrate to the Lakehouse](/company/partners/consulting-and-si/candsi-partner-program)
        * [Data PartnersAccess the ecosystem of data consumers](/company/partners/data-partner-program)
        * [Partner SolutionsFind custom industry and migration solutions](/company/partners/consulting-and-si/partner-solutions)
        * [Built on DatabricksBuild, market and grow your business](/company/partners/built-on-partner-program)

  * Product

    *       * Databricks Platform

        * [Platform OverviewA unified platform for data, analytics and AI](/product/data-intelligence-platform)
        * [Data ManagementData reliability, security and performance](/product/delta-lake-on-databricks)
        * [SharingAn open, secure, zero-copy sharing for all data](/product/delta-sharing)
        * [Data WarehousingServerless data warehouse for SQL analytics](/product/databricks-sql)
        * [GovernanceUnified governance for all data, analytics and AI assets](/product/unity-catalog)
        * [Data EngineeringETL and orchestration for batch and streaming data](/product/data-engineering)
        * [Artificial IntelligenceBuild and deploy ML and GenAI applications](/product/artificial-intelligence)
        * [Data ScienceCollaborative data science at scale](/product/data-science)
        * [Business IntelligenceIntelligent analytics for real-world data](https://www.databricks.com/product/business-intelligence)
        * [Application DevelopmentQuickly build secure data and AI apps](/product/databricks-apps)
        * [DatabasePostgres for data apps and AI agents](/product/lakebase)

      * Integrations and Data

        * [MarketplaceOpen marketplace for data, analytics and AI](/product/marketplace)
        * [IDE IntegrationsBuild on the Lakehouse in your favorite IDE](/product/data-science/ide-integrations)
        * [Partner ConnectDiscover and integrate with the Databricks ecosystem](/partnerconnect)

      * Pricing

        * [Databricks PricingExplore product pricing, DBUs and more](/product/pricing)
        * [Cost CalculatorEstimate your compute costs on any cloud](/product/pricing/product-pricing/instance-types)

      * Open Source

        * [Open Source TechnologiesLearn more about the innovations behind the platform](/product/open-source)

  * Solutions

    *       * Databricks for Industries

        * [Communications](/solutions/industries/communications)
        * [Media and Entertainment](/solutions/industries/media-and-entertainment)
        * [Financial Services](/solutions/industries/financial-services)
        * [Public Sector](/solutions/industries/public-sector)
        * [Healthcare & Life Sciences](/solutions/industries/healthcare-and-life-sciences)
        * [Retail](/solutions/industries/retail-industry-solutions)
        * [Manufacturing](/solutions/industries/manufacturing-industry-solutions)
        * [See All Industries](/solutions)

      * Cross Industry Solutions

        * [Cybersecurity](/solutions/industries/cybersecurity)
        * [Marketing](/solutions/industries/marketing)

      * Migration & Deployment

        * [Data Migration](/solutions/migration)
        * [Professional Services](/professional-services)

      * Solution Accelerators

        * [Explore AcceleratorsMove faster toward outcomes that matter](/solutions/accelerators)

  * Resources

    *       * Learning

        * [TrainingDiscover curriculum tailored to your needs](https://www.databricks.com/learn/training/home)
        * [Databricks AcademySign in to the Databricks learning platform](https://www.databricks.com/learn/training/login)
        * [CertificationGain recognition and differentiation](https://www.databricks.com/learn/training/certification)
        * [Free EditionLearn professional Data and AI tools for free](/learn/free-edition)
        * [University AllianceWant to teach Databricks? See how.](/university)

      * Events

        * [Data + AI Summit](https://www.databricks.com/dataaisummit)
        * [Data + AI World Tour](/dataaisummit/worldtour)
        * [Data Intelligence Days](/lp/data-intelligence-days)
        * [Event Calendar](/events)

      * Blog and Podcasts

        * [Databricks BlogExplore news, product announcements, and more](/blog)
        * [Databricks Mosaic Research BlogDiscover the latest in our Gen AI research](/blog/category/generative-ai/mosaic-research)
        * [Data Brew PodcastLet’s talk data!](/discover/data-brew)
        * [Champions of Data + AI PodcastInsights from data leaders powering innovation](/discover/champions-of-data-and-ai)

      * Get Help

        * [Customer Support](https://www.databricks.com/support)
        * [Documentation](https://docs.databricks.com/en/index.html)
        * [Community](https://community.databricks.com/s/)

      * Dive Deep

        * [Resource Center](/resources)
        * [Demo Center](/resources/demos)
        * [Architecture Center](/resources/architectures)

  * About

    *       * Company

        * [Who We Are](/company/about-us)
        * [Our Team](/company/leadership-team)
        * [Databricks Ventures](/databricks-ventures)
        * [Contact Us](/company/contact)

      * Careers

        * [Working at Databricks](/company/careers)
        * [Open Jobs](/company/careers/open-positions)

      * Press

        * [Awards and Recognition](/company/awards-and-recognition)
        * [Newsroom](/company/newsroom)

      * Security and Trust

        * [Security and Trust](/trust)




  * Ready to get started?

  * [Get a Demo](/resources/demos)



  * [Login](https://login.databricks.com/?dbx_source=www&itm=main-cta-login&l=en-EN)
  * [Contact Us](/company/contact)
  * [Try Databricks](https://www.databricks.com/signup?dbx_source=www&itm_data=dbx-web-nav&l=en-EN)



  1. [Blog](/blog)
  2. /

[Open Source](/blog/category/engineering/open-source)
  3. /

Article




* * *

# Spark Structured Streaming

![spark-2-structured-streaming-OG](https://www.databricks.com/sites/default/files/2016/07/spark-2-structured-streaming-OG.png?v=1660758008)

Published: July 28, 2016

[Open Source](/blog/category/engineering/open-source)12 min read

by [Matei Zaharia](/blog/author/matei-zaharia), [Tathagata Das](/blog/author/tdas), [Michael Lumb](/blog/author/michael-lumb) and [Reynold Xin](/blog/author/reynold-xin)

Share this post

  * [](https://www.linkedin.com/shareArticle?mini=true&url=https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html&summary=&source=)
  * [](https://twitter.com/intent/tweet?text=https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html)
  * [](https://www.facebook.com/sharer/sharer.php?u=https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html)



Keep up with us

Subscribe

 _Free Edition has replaced Community Edition, offering enhanced features at no cost. Start using_[ _Free Edition_](https://login.databricks.com/?intent=SIGN_UP&amp;signup_experience_step=EXPRESS&amp;provider=DB_FREE_TIER&amp;dbx_source=www) _today._  


Apache Spark 2.0 adds the first version of a new higher-level API, Structured Streaming, for building [continuous applications](https://www.databricks.com/blog/2016/07/28/continuous-applications-evolving-streaming-in-apache-spark-2-0.html). The main goal is to make it easier to build _end-to-end_ streaming applications, which integrate with storage, serving systems, and batch jobs in a consistent and fault-tolerant way. In this post, we explain why this is hard to do with current distributed streaming engines, and introduce Structured Streaming.

## Why Streaming is Difficult

At first glance, building a distributed streaming engine might seem as simple as launching a set of servers and pushing data between them. Unfortunately, distributed stream processing runs into multiple complications that don’t affect simpler computations like batch jobs.

To start, consider a simple application: we receive (phone_id, time, action) events from a mobile app, and want to count how many actions of each type happened each hour, then store the result in MySQL. If we were running this application as a batch job and had a table with all the input events, we could express it as the following SQL query:

In a distributed streaming engine, we might set up nodes to process the data in a "map-reduce" pattern, as shown below. Each node in the first layer reads a partition of the input data (say, the stream from one set of phones), then hashes the events by (action, hour) to send them to a reducer node, which tracks that group’s count and periodically updates MySQL.

Unfortunately, this type of design can introduce quite a few challenges:

  1. **Consistency** : This distributed design can cause records to be processed in one part of the system before they’re processed in another, leading to nonsensical results. For example, suppose our app sends an "open" event when users open it, and a "close" event when closed. If the reducer node responsible for "open" is slower than the one for "close", we might see a _higher total count of "closes" than "opens" in MySQL_ , which would not make sense. The image above actually shows one such example.
  2. **Fault tolerance** : What happens if one of the mappers or reducers fails? A reducer should not count an action in MySQL twice, but should somehow know how to request old data from the mappers when it comes up. Streaming engines go through a great deal of trouble to provide strong semantics here, at least _within_ the engine. In many engines, however, keeping the result consistent in external storage is left to the user.
  3. **Out-of-order data** : In the real world, data from different sources can come out of order: for example, a phone might upload its data hours late if it's out of coverage. Just writing the reducer operators to assume data arrives in order of time fields will not work---they need to be prepared to receive out-of-order data, and to update the results in MySQL accordingly.



In most current streaming systems, some or all of these concerns are left to the user. This is unfortunate because these issues---how the application interacts with the outside world---are some of the hardest to reason about and get right. In particular, there is no easy way to get semantics as simple as the SQL query above.

## Structured Streaming Model

In Structured Streaming, we tackle the issue of semantics head-on by making a strong guarantee about the system: _at any time, the output of the application is equivalent to executing a batch job on a prefix of the data_. For example, in our monitoring application, the result table in MySQL will always be equivalent to taking a prefix of each phone’s update stream (whatever data made it to the system so far) and running the SQL query we showed above. There will never be "open" events counted faster than "close" events, duplicate updates on failure, etc. Structured Streaming automatically handles consistency and reliability both within the engine and in interactions with external systems (e.g. updating MySQL transactionally).

This _prefix integrity_ guarantee makes it easy to reason about the three challenges we identified. In particular:

  1. Output tables are **always consistent** with all the records in a prefix of the data. For example, as long as each phone uploads its data as a sequential stream (e.g., to the same partition in Apache Kafka), we will always process and count its events in order.
  2. **Fault tolerance** is handled holistically by Structured Streaming, including in interactions with output sinks. This was a major goal in supporting [continuous applications](https://www.databricks.com/blog/2016/07/28/continuous-applications-evolving-streaming-in-apache-spark-2-0.html).
  3. The effect of **out-of-order data** is clear. We know that the job outputs counts grouped by action and time for a prefix of the stream. If we later receive more data, we might see a time field for an hour in the past, and we will simply update its respective row in MySQL. Structured Streaming also supports APIs for filtering out overly old data if the user wants. But fundamentally, out-of-order data is not a "special case": the query says to group by time field, and seeing an old time is no different than seeing a repeated action.



The last benefit of Structured Streaming is that the API is very easy to use: it is simply Spark's [DataFrame and Dataset](https://www.databricks.com/blog/2016/01/04/introducing-apache-spark-datasets.html) API. Users just describe the query they want to run, the input and output locations, and optionally a few more details. The system then runs their query incrementally, maintaining enough state to recover from failure, keep the results consistent in external storage, etc. For example, here is how to write our streaming monitoring application:

This code is nearly identical to the batch version below---only the "read" and "write" changed:

The next sections explain the model in more detail, as well as the API.

## Model Details

Conceptually, Structured Streaming treats all the data arriving as an unbounded **input table**. Each new item in the stream is like a row appended to the input table. We won’t actually retain all the input, but our results will be equivalent to having all of it and running a batch job.  


  
The developer then defines a **query** on this input table, as if it were a static table, to compute a final **result table** that will be written to an output sink. Spark automatically converts this batch-like query to a streaming execution plan. This is called _incrementalization:_ Spark figures out what state needs to be maintained to update the result each time a record arrives. Finally, developers specify **triggers** to control when to update the results. Each time a trigger fires, Spark checks for new data (new row in the input table), and incrementally updates the result.

The last part of the model is **output modes**. Each time the result table is updated, the developer wants to write the changes to an external system, such as S3, HDFS, or a database. We usually want to write output incrementally. For this purpose, Structured Streaming provides three output modes:

  * **Append:** Only the new rows appended to the result table since the last trigger will be written to the external storage. This is applicable only on queries where existing rows in the result table cannot change (e.g. a map on an input stream).
  * **Complete** : The entire updated result table will be written to external storage.
  * **Update** : Only the rows that were updated in the result table since the last trigger will be changed in the external storage. This mode works for output sinks that can be updated in place, such as a MySQL table.



Let’s see how we can run our mobile monitoring application in this model. Our batch query is to compute a count of actions grouped by (action, hour). To run this query incrementally, Spark will maintain some state with the counts for each pair so far, and update when new records arrive. For each record changed, it will then output data according to its output mode. The figure below shows this execution using the Update output mode:

At every trigger point, we take the previous grouped counts and update them with new data that arrived since the last trigger to get a new result table. We then emit only the changes required by our output mode to the sink---here, we update the records for (action, hour) pairs that changed during that trigger in MySQL (shown in red).

Note that the system also automatically handles late data. In the figure above, the "open" event for phone3, which happened at 1:58 on the phone, only gets to the system at 2:02. Nonetheless, even though it’s past 2:00, we update the record for 1:00 in MySQL. However, the prefix integrity guarantee in Structured Streaming ensures that we process the records from each source _in the order they arrive_. For example, because phone1’s "close" event arrives after its "open" event, we will always update the "open" count before we update the "close" count.

## Fault Recovery and Storage System Requirements

Structured Streaming keeps its results valid even if machines fail. To do this, it places two requirements on the input sources and output sinks:

  1. Input sources must be _replayable_ , so that recent data can be re-read if the job crashes. For example, message buses like Amazon Kinesis and Apache Kafka are replayable, as is the file system input source. Only a few minutes’ worth of data needs to be retained; Structured Streaming will maintain its own internal state after that.
  2. Output sinks must support _transactional updates_ , so that the system can make a set of records appear atomically. The current version of Structured Streaming implements this for file sinks, and we also plan to add it for common databases and key-value stores.



We found that most Spark applications already use sinks and sources with these properties, because users want their jobs to be reliable.

Apart from these requirements, Structured Streaming will manage its internal state in a reliable storage system, such as S3 or HDFS, to store data such as the running counts in our example. Given these properties, Structured Streaming will enforce prefix integrity end-to-end.

## Structured Streaming API

Structured Streaming is integrated into Spark’s [Dataset and DataFrame APIs](https://www.databricks.com/blog/2016/07/14/a-tale-of-three-apache-spark-apis-rdds-dataframes-and-datasets.html); in most cases, you only need to add a few method calls to run a streaming computation. It also adds new operators for windowed aggregation and for setting parameters of the execution model (e.g. output modes). In [Apache Spark 2.0](https://www.databricks.com/blog/2016/07/26/introducing-apache-spark-2-0.html), we’ve built an alpha version of the system with the core APIs. More operators, such as sessionization, will come in future releases.

### API Basics

Streams in Structured Streaming are represented as DataFrames or Datasets with the isStreaming property set to true. You can create them using special read methods from various sources. For example, suppose we wanted to read data in our monitoring application from JSON files uploaded to Amazon S3. The code below shows how to do this in Scala:

Our resulting DataFrame, inputDF, is our input table, which will be continuously extended with new rows as new files are added to the directory. The table has two columns---time and action. Now you can use the usual DataFrame/Dataset operations to transform the data. In our example, we want to count action types each hour. To do that we have to group the data by action and 1 hours windows of time.

The new DataFrame countsDF is our result table, which has the columns action, window, and count, and will be continuously updated when the query is started. Note that this transformation would give hourly counts even if inputDF was a static table. This allows developers to test their business logic on static datasets and seamless apply them on streaming data without changing the logic.

Finally, we tell the engine to write this table to a sink and start the streaming computation.

The returned `query` is a StreamingQuery, a handle to the active streaming execution and can be used to manage and monitor the execution.

Beyond these basics, there are many more operations that can be done in Structured Streaming.

### Mapping, Filtering and Running Aggregations

Structured Streaming programs can use DataFrame and Dataset’s existing methods to transform data, including map, filter, select, and others. In addition, running (or infinite) aggregations, such as a `count` from the beginning of time, are available through the existing APIs. This is what we used in our monitoring application above.

### Windowed Aggregations on Event Time

Streaming applications often need to compute data on various types of _windows_ , including _sliding windows_ , which overlap with each other (e.g. a 1-hour window that advances every 5 minutes), and tumbling windows, which do not (e.g. just every hour). In Structured Streaming, _windowing is simply represented as a group-by_. Each input event can be mapped to one or more windows, and simply results in updating one or more result table rows.

Windows can be specified using the window function in DataFrames. For example, we could change our monitoring job to count actions by sliding windows as follows:

Whereas our previous application outputted results of the form (hour, action, count), this new one will output results of the form (window, action, count), such as ("1:10-2:10", "open", 17). If a late record arrives, we will update all the corresponding windows in MySQL. And unlike in many other systems, windowing is not just a special operator for streaming computations; we can run the same code in a batch job to group data in the same way.

Windowed aggregation is one area where we will continue to expand Structured Streaming. In particular, in Spark 2.1, we plan to add _watermarks_ , a feature for dropping overly old data when sufficient time has passed. Without this type of feature, the system might have to track state for all old windows, which would not scale as the application runs. In addition, we plan to add support for _session-based windows_ , i.e. grouping the events from one source into variable-length sessions according to business logic.

### Joining Streams with Static Data

Because Structured Streaming simply uses the DataFrame API, it is straightforward to join a stream against a static DataFrame, such as an Apache Hive table:

Moreover, the static DataFrame could itself be computed using a Spark query, allowing us to mix batch and streaming computations.

### Interactive Queries

Structured Streaming can expose results directly to interactive queries through Spark’s JDBC server. In Spark 2.0, there is a rudimentary "memory" output sink for this purpose that is not designed for large data volumes. However, in future releases, this will let you write query results to an in-memory Spark SQL table, and run queries directly against it.

## Comparison With Other Engines

To show what’s unique about Structured Streaming, the next table compares it with several other systems. As we discussed, Structured Streaming’s strong guarantee of prefix integrity makes it equivalent to batch jobs and easy to integrate into larger applications. Moreover, building on Spark enables integration with batch and interactive queries.

## Conclusion

Structured Streaming promises to be a much simpler model for building end-to-end real-time applications, built on the features that work best in [Spark Streaming](https://www.databricks.com/blog/2015/07/30/diving-into-apache-spark-streamings-execution-model.html). Although Structured Streaming is in alpha for Apache Spark 2.0, we hope this post encourages you to try it out.

Long-term, much like the [DataFrame API](https://www.databricks.com/blog/2015/02/17/introducing-dataframes-in-spark-for-large-scale-data-science.html), we expect Structured Streaming to complement Spark Streaming by providing a more restricted but higher-level interface. If you are running Spark Streaming today, don’t worry---it will continue to be supported. But we believe that Structured Streaming can open up real-time computation to many more users.

Structured Streaming is also fully supported on Databricks, including in the free[ Databricks Community Edition](https://www.databricks.com/signup?dbx_source=www&itm_data=dbx-web&l=en-EN).

## Read More

In addition, the following resources cover Structured Streaming:

  * [Structuring Spark: DataFrames, Datasets and Streaming](https://www.databricks.com/dataaisummit)
  * [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
  * [Spark 2.0 and Structured Streaming](https://www.databricks.com/dataaisummit)
  * [A Deep Dive Into Structured Streaming](https://www.databricks.com/dataaisummit)



Keep up with us

Subscribe

Share this post

  * [](https://www.linkedin.com/shareArticle?mini=true&url=https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html&summary=&source=)
  * [](https://twitter.com/intent/tweet?text=https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html)
  * [](https://www.facebook.com/sharer/sharer.php?u=https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html)



## Never miss a Databricks post

Subscribe to the categories you care about and get the latest posts delivered to your inbox

## Sign up

## What's next?

[![GGML GGUF File Format Vulnerabilities](https://www.databricks.com/sites/default/files/2024-03/ggml-gguf-file-format-vulnerabilities-og.png?v=1711052506)Open SourceMarch 22, 2024/10 min readGGML GGUF File Format Vulnerabilities](/blog/ggml-gguf-file-format-vulnerabilities)

[![databricks x google cloud](https://www.databricks.com/sites/default/files/2025-01/bigquery-adds-first-party-support-delta-lake.png?v=1736898323)Open SourceJune 5, 2024/3 min readBigQuery adds first-party support for Delta Lake](/blog/bigquery-adds-first-party-support-delta-lake)

[![databricks logo](https://www.databricks.com/sites/default/files/2023-08/databricks-default.png?v=1712162038)](https://www.databricks.com/)

Why Databricks

Discover

  * [For Executives](/why-databricks/executives)
  * [For Startups](/product/startups)
  * [Lakehouse Architecture](/product/data-lakehouse)
  * [Mosaic Research](/research/mosaic)



Customers

  * [Customer Stories](https://www.databricks.com/customers)



Partners

  * [Cloud Providers](/company/partners/cloud-partners)
  * [Technology Partners](/company/partners/technology-partner-program)
  * [Data Partners](/company/partners/data-partner-program)
  * [Built on Databricks](/company/partners/built-on-partner-program)
  * [Consulting & System Integrators](/company/partners/consulting-and-si)
  * [C&SI Partner Program](/company/partners/consulting-and-si/candsi-partner-program)
  * [Partner Solutions](/company/partners/consulting-and-si/partner-solutions)



Why Databricks

Discover

  * [For Executives](/why-databricks/executives)
  * [For Startups](/product/startups)
  * [Lakehouse Architecture](/product/data-lakehouse)
  * [Mosaic Research](/research/mosaic)



Customers

  * [Customer Stories](https://www.databricks.com/customers)



Partners

  * [Cloud Providers](/company/partners/cloud-partners)
  * [Technology Partners](/company/partners/technology-partner-program)
  * [Data Partners](/company/partners/data-partner-program)
  * [Built on Databricks](/company/partners/built-on-partner-program)
  * [Consulting & System Integrators](/company/partners/consulting-and-si)
  * [C&SI Partner Program](/company/partners/consulting-and-si/candsi-partner-program)
  * [Partner Solutions](/company/partners/consulting-and-si/partner-solutions)



Product

Databricks Platform

  * [Platform Overview](/product/data-intelligence-platform)
  * [Sharing](/product/delta-sharing)
  * [Governance](/product/unity-catalog)
  * [Artificial Intelligence](/product/artificial-intelligence)
  * [Business Intelligence](https://www.databricks.com/product/business-intelligence)
  * [Database](/product/lakebase)
  * [Data Management](/product/delta-lake-on-databricks)
  * [Data Warehousing](/product/databricks-sql)
  * [Data Engineering](/product/data-engineering)
  * [Data Science](/product/data-science)
  * [Application Development](/product/databricks-apps)



Pricing

  * [Pricing Overview](/product/pricing)
  * [Pricing Calculator](/product/pricing/product-pricing/instance-types)



[Open Source](/product/open-source)

Integrations and Data

  * [Marketplace](/product/marketplace)
  * [IDE Integrations](/product/data-science/ide-integrations)
  * [Partner Connect](/partnerconnect)



Product

Databricks Platform

  * [Platform Overview](/product/data-intelligence-platform)
  * [Sharing](/product/delta-sharing)
  * [Governance](/product/unity-catalog)
  * [Artificial Intelligence](/product/artificial-intelligence)
  * [Business Intelligence](https://www.databricks.com/product/business-intelligence)
  * [Database](/product/lakebase)
  * [Data Management](/product/delta-lake-on-databricks)
  * [Data Warehousing](/product/databricks-sql)
  * [Data Engineering](/product/data-engineering)
  * [Data Science](/product/data-science)
  * [Application Development](/product/databricks-apps)



Pricing

  * [Pricing Overview](/product/pricing)
  * [Pricing Calculator](/product/pricing/product-pricing/instance-types)



Open Source

Integrations and Data

  * [Marketplace](/product/marketplace)
  * [IDE Integrations](/product/data-science/ide-integrations)
  * [Partner Connect](/partnerconnect)



Solutions

Databricks For Industries

  * [Communications](/solutions/industries/communications)
  * [Financial Services](/solutions/industries/financial-services)
  * [Healthcare and Life Sciences](/solutions/industries/healthcare-and-life-sciences)
  * [Manufacturing](/solutions/industries/manufacturing-industry-solutions)
  * [Media and Entertainment](/solutions/industries/media-and-entertainment)
  * [Public Sector](/solutions/industries/federal-government)
  * [Retail](/solutions/industries/retail-industry-solutions)
  * [View All](/solutions)



Cross Industry Solutions

  * [Cybersecurity](/solutions/industries/cybersecurity)
  * [Marketing](/solutions/industries/marketing)



[Data Migration](/solutions/migration)

[Professional Services](/professional-services)

[Solution Accelerators](/solutions/accelerators)

Solutions

Databricks For Industries

  * [Communications](/solutions/industries/communications)
  * [Financial Services](/solutions/industries/financial-services)
  * [Healthcare and Life Sciences](/solutions/industries/healthcare-and-life-sciences)
  * [Manufacturing](/solutions/industries/manufacturing-industry-solutions)
  * [Media and Entertainment](/solutions/industries/media-and-entertainment)
  * [Public Sector](/solutions/industries/federal-government)
  * [Retail](/solutions/industries/retail-industry-solutions)
  * [View All](/solutions)



Cross Industry Solutions

  * [Cybersecurity](/solutions/industries/cybersecurity)
  * [Marketing](/solutions/industries/marketing)



Data Migration

Professional Services

Solution Accelerators

Resources

[Documentation](https://docs.databricks.com/en/index.html)

[Customer Support](https://www.databricks.com/support)

[Community](https://community.databricks.com/)

Learning

  * [Training](/learn/training/home)
  * [Certification](https://www.databricks.com/learn/training/certification)
  * [Free Edition](/learn/free-edition)
  * [University Alliance](/university)
  * [Databricks Academy Login](https://www.databricks.com/learn/training/login)



Events

  * [Data + AI Summit](/dataaisummit)
  * [Data + AI World Tour](/dataaisummit/worldtour)
  * [Data Intelligence Days](/lp/data-intelligence-days)
  * [Event Calendar](/events)



Blog and Podcasts

  * [Databricks Blog](/blog)
  * [Databricks Mosaic Research Blog](https://www.databricks.com/blog/category/generative-ai/mosaic-research)
  * [Data Brew Podcast](/discover/data-brew)
  * [Champions of Data & AI Podcast](/discover/champions-of-data-and-ai)



Resources

Documentation

Customer Support

Community

Learning

  * [Training](/learn/training/home)
  * [Certification](https://www.databricks.com/learn/training/certification)
  * [Free Edition](/learn/free-edition)
  * [University Alliance](/university)
  * [Databricks Academy Login](https://www.databricks.com/learn/training/login)



Events

  * [Data + AI Summit](/dataaisummit)
  * [Data + AI World Tour](/dataaisummit/worldtour)
  * [Data Intelligence Days](/lp/data-intelligence-days)
  * [Event Calendar](/events)



Blog and Podcasts

  * [Databricks Blog](/blog)
  * [Databricks Mosaic Research Blog](https://www.databricks.com/blog/category/generative-ai/mosaic-research)
  * [Data Brew Podcast](/discover/data-brew)
  * [Champions of Data & AI Podcast](/discover/champions-of-data-and-ai)



About

Company

  * [Who We Are](/company/about-us)
  * [Our Team](/company/leadership-team)
  * [Databricks Ventures](/databricks-ventures)
  * [Contact Us](/company/contact)



Careers

  * [Open Jobs](/company/careers/open-positions)
  * [Working at Databricks](/company/careers)



Press

  * [Awards and Recognition](/company/awards-and-recognition)
  * [Newsroom](/company/newsroom)



[Security and Trust](/trust)

About

Company

  * [Who We Are](/company/about-us)
  * [Our Team](/company/leadership-team)
  * [Databricks Ventures](/databricks-ventures)
  * [Contact Us](/company/contact)



Careers

  * [Open Jobs](/company/careers/open-positions)
  * [Working at Databricks](/company/careers)



Press

  * [Awards and Recognition](/company/awards-and-recognition)
  * [Newsroom](/company/newsroom)



Security and Trust

[![databricks logo](https://www.databricks.com/sites/default/files/2023-08/databricks-default.png?v=1712162038)](https://www.databricks.com/)

Databricks Inc.  
160 Spear Street, 15th Floor  
San Francisco, CA 94105  
1-866-330-0121

  * [](https://www.linkedin.com/company/databricks)
  * [](https://www.facebook.com/pages/Databricks/560203607379694)
  * [](https://twitter.com/databricks)
  * [](https://www.databricks.com/feed)
  * [](https://www.glassdoor.com/Overview/Working-at-Databricks-EI_IE954734.11,21.htm)
  * [](https://www.youtube.com/@Databricks)



![](https://www.databricks.com/sites/default/files/2021/02/telco-icon-2.png?v=1715274112)

[See Careers  
at Databricks](https://www.databricks.com/company/careers)

  * [](https://www.linkedin.com/company/databricks)
  * [](https://www.facebook.com/pages/Databricks/560203607379694)
  * [](https://twitter.com/databricks)
  * [](https://www.databricks.com/feed)
  * [](https://www.glassdoor.com/Overview/Working-at-Databricks-EI_IE954734.11,21.htm)
  * [](https://www.youtube.com/@Databricks)



© Databricks 2025. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the [Apache Software Foundation](https://www.apache.org/).

  * [Privacy Notice](https://www.databricks.com/legal/privacynotice)
  * |[Terms of Use](https://www.databricks.com/legal/terms-of-use)
  * |[Modern Slavery Statement](https://www.databricks.com/legal/modern-slavery-policy-statement)
  * |[California Privacy](https://www.databricks.com/legal/supplemental-privacy-notice-california-residents)
  * |Your Privacy Choices
  * ![](https://www.databricks.com/sites/default/files/2022-12/gpcicon_small.png)


