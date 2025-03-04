# Build new AI applications with Azure SQL Database

## Overview
This lab will guide you through creating a RAG application using relational data, Azure OpenAI, and the Azure SQL Database. The workshop utilizes the always free Azure SQL Database and the ability to call external REST endpoints via a system stored procedure ([sp_invoke_external_rest_endpoint](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-invoke-external-rest-endpoint-transact-sql?view=azuresqldb-current&tabs=request-headers)).

The lab contains 8 chapters:
* The Azure Portal and connecting to your free Azure SQL Database
* Getting started with REST in the database
* Creating embeddings for relational data with Azure OpenAI
* Using Azure SQL's VECTOR_DISTANCE for similarity searches
* Create a chat app on your data with RAG and Azure SQL
* Securing your data
* GraphRAG and the Azure SQL Database
* Extra Credit Activities

## Prerequisites

**Software**
 - Visual Studio Code with the SQL Extension

**Services**
 - Azure OpenAI instance with a text-embedding-ada-002 deployment and a gpt-4 deployment.
 - An Azure SQL Database

**Key Information Needed**
 - Azure SQL Database Server Name
 - Azure SQL Database Name
 - Azure OpenAI Endpoint Name
 - Azute OpenAI Endpoint Key

## Getting Started
To begin the lab, clone this repository and follow the instructions in each section. Make sure to check the [deck] directory for additional materials.

## Contributing
Contributions to this lab are welcome! Please read the `CONTRIBUTING.md` file for guidelines on how to contribute.

## License
This lab is provided under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments
A special thanks to all the contributors and maintainers of this lab. 

## Contact
For any queries or feedback regarding the lab, please open an issue in this repository or contact the lab maintainers directly.

Happy coding and learning!
