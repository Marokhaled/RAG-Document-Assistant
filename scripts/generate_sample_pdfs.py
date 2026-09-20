import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

documents = [
    {
        "filename": "CS101_Operating_Systems_Guide.pdf",
        "title": "CS101: Operating Systems & Kernel Concepts",
        "pages": [
            {
                "heading": "Chapter 1: Operating Systems & Process Management",
                "content": """
Operating system kernels manage system hardware, CPU scheduling, and process execution. 
A process is an instance of a computer program being executed. Every process has a Process Control Block (PCB) containing process state, program counter, CPU registers, memory limits, and list of open files.
Process states include New, Ready, Running, Waiting, and Terminated.
Context switching is the mechanism of saving the CPU state of a running process into its PCB and restoring the state of another process to resume execution.
CPU scheduling algorithms include First-Come First-Served (FCFS), Shortest Job First (SJF), Round Robin (RR), and Priority Scheduling.
"""
            },
            {
                "heading": "Chapter 2: Threads, Synchronization & Deadlocks",
                "content": """
A thread is a lightweight unit of CPU utilization containing its own thread ID, program counter, register set, and stack. Multiple threads within the same process share code, data, and OS resources.
User-level threads are managed without OS kernel support, whereas kernel-level threads are managed directly by the operating system kernel.
Inter-Process Communication (IPC) allows processes to communicate via shared memory or message passing.
Concurrency issues arise when processes access shared data concurrently. Mutex locks and semaphores provide mutual exclusion.
A deadlock occurs when a set of processes are blocked because each process holds a resource and waits for another resource held by another process.
The four necessary conditions for deadlock are: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.
"""
            },
            {
                "heading": "Chapter 3: Memory Management & Virtual Memory",
                "content": """
Memory management keeps track of each byte of memory in the system and handles allocation to active processes.
Contiguous memory allocation assigns consecutive blocks of memory to processes using base and limit registers.
Paging is a memory management scheme that eliminates contiguous allocation requirements by dividing physical memory into fixed-size blocks called frames and logical memory into pages.
The Memory Management Unit (MMU) translates logical addresses into physical addresses using page tables.
Virtual memory is a memory management technique that provides an idealized abstraction of storage, allowing execution of processes that exceed physical memory size.
When a process accesses a page not currently in physical memory, a page fault exception occurs, triggering the OS to load the page from disk into RAM.
Page replacement algorithms include First-In First-Out (FIFO), Least Recently Used (LRU), and Optimal Page Replacement.
"""
            },
            {
                "heading": "Chapter 4: File Systems & Storage Management",
                "content": """
File systems provide a logical view of storage resources. File attributes include name, identifier, type, location, size, and protection permissions.
Directory structures organize files logically into single-level, two-level, or tree-structured directories.
Disk allocation methods include Contiguous Allocation, Linked Allocation, and Indexed Allocation (inode-based).
Disk scheduling algorithms optimize disk read/write head movement across tracks. Examples include FCFS, Shortest Seek Time First (SSTF), SCAN (Elevator Algorithm), and C-SCAN.
"""
            }
        ]
    },
    {
        "filename": "CS102_Database_Management_Systems.pdf",
        "title": "CS102: Relational Database Management Systems & SQL",
        "pages": [
            {
                "heading": "Chapter 1: Relational Model & SQL",
                "content": """
A Database Management System (DBMS) is software designed to define, manipulate, retrieve, and manage structured data.
The relational model represents data as tables consisting of rows (tuples) and columns (attributes).
Primary key uniquely identifies each record in a relation. Foreign key establishes referential integrity between tables.
Relational algebra operations include Selection (sigma), Projection (pi), Union, Set Difference, Cartesian Product, and Natural Join.
Data Definition Language (DDL) commands include CREATE, ALTER, DROP, and TRUNCATE.
Data Manipulation Language (DML) commands include SELECT, INSERT, UPDATE, and DELETE.
"""
            },
            {
                "heading": "Chapter 2: Relational Database Normalization",
                "content": """
Database normalization minimizes data redundancy and eliminates insertion, update, and deletion anomalies.
Functional Dependency (X -> Y) means X uniquely determines Y.
First Normal Form (1NF): Requires atomic attribute values with no repeating groups.
Second Normal Form (2NF): Requires 1NF and no partial dependencies where non-prime attributes depend on a subset of a composite primary key.
Third Normal Form (3NF): Requires 2NF and no transitive dependencies where non-prime attributes depend on other non-prime attributes.
Boyce-Codd Normal Form (BCNF): A stricter version of 3NF where for every functional dependency X -> Y, X must be a super key.
"""
            },
            {
                "heading": "Chapter 3: Transactions & ACID Properties",
                "content": """
A transaction is a logical unit of database processing executed as a single unit.
ACID properties guarantee reliability in database transactions:
Atomicity: All operations in a transaction succeed, or the entire transaction is rolled back.
Consistency: Database transitions from one valid state to another valid state preserving integrity constraints.
Isolation: Concurrent transactions execute independently without interfering with each other.
Durability: Committed transactions persist permanently even during system failures.
Concurrency control protocols such as Two-Phase Locking (2PL) and Timestamp Ordering ensure serializability.
Deadlocks in DBMS occur when transactions wait indefinitely for locks held by each other.
"""
            },
            {
                "heading": "Chapter 4: Indexing & Query Optimization",
                "content": """
Database indexing improves data retrieval speed at the cost of additional storage and write overhead.
B-Trees and B+ Trees are balanced search trees widely used for disk-based indexing because they maintain sorted data and allow efficient search, insertion, and deletion in O(log N) time.
Hash indexes provide O(1) average time complexity for exact match equality queries.
Query optimizers evaluate query execution plans and choose optimal join algorithms such as Nested Loop Join, Hash Join, and Sort-Merge Join based on cost estimation.
"""
            }
        ]
    },
    {
        "filename": "CS103_Computer_Networks_Handout.pdf",
        "title": "CS103: Computer Networks & Internet Protocols",
        "pages": [
            {
                "heading": "Chapter 1: OSI 7-Layer Architecture",
                "content": """
The Open Systems Interconnection (OSI) model standardizes network communication functions across 7 layers:
Layer 7 - Application: User interface services (HTTP, FTP, SMTP, DNS).
Layer 6 - Presentation: Data formatting, encryption, and compression (TLS, JPEG, ASCII).
Layer 5 - Session: Manages sessions between applications.
Layer 4 - Transport: End-to-end communication, segmentation, flow control (TCP, UDP).
Layer 3 - Network: Logical addressing and routing across subnets (IP, ICMP, ARP).
Layer 2 - Data Link: Framing, MAC addressing, error detection (Ethernet, Wi-Fi).
Layer 1 - Physical: Bitstream transmission over physical media (Cables, Fiber optics).
"""
            },
            {
                "heading": "Chapter 2: Transport Layer & TCP Handshake",
                "content": """
The Transport Layer provides process-to-process communication using port numbers.
Transmission Control Protocol (TCP) is a connection-oriented, reliable protocol providing ordered byte delivery, error checking, and flow control.
User Datagram Protocol (UDP) is a connectionless, lightweight, unreliable protocol suitable for real-time video streaming and DNS queries.
The TCP 3-Way Handshake establishes a connection between client and server:
1. Client sends SYN (Synchronize) packet with initial sequence number ISN.
2. Server responds with SYN-ACK (Synchronize-Acknowledge) packet.
3. Client sends ACK (Acknowledge) packet, establishing the TCP connection.
TCP sliding window protocol manages flow control to prevent receiver buffer overflow.
"""
            },
            {
                "heading": "Chapter 3: Network Layer, IP Addressing & Routing",
                "content": """
The Network layer uses IP addresses to route packets across interconnected networks.
IPv4 uses 32-bit addresses written in dotted decimal format, supporting up to 4.3 billion unique addresses. IPv6 uses 128-bit hexadecimal addresses.
Subnetting divides a larger network into smaller subnets using subnet masks and Classless Inter-Domain Routing (CIDR) notation.
Routing algorithms determine optimal paths for data packets:
Distance Vector Routing (e.g., RIP) uses Bellman-Ford algorithm based on hop counts.
Link State Routing (e.g., OSPF) uses Dijkstra's shortest path algorithm based on link costs.
Address Resolution Protocol (ARP) resolves IP addresses to physical MAC addresses.
"""
            },
            {
                "heading": "Chapter 4: Application Layer & Web Protocols",
                "content": """
Hypertext Transfer Protocol (HTTP) is the foundation of web data exchange operating over TCP port 80.
HTTP/1.1 introduced persistent connections (keep-alive). HTTP/2 added multiplexing over single TCP connection. HTTP/3 utilizes QUIC protocol over UDP.
HTTPS encrypts HTTP traffic using TLS/SSL cryptographic protocols over TCP port 443.
Domain Name System (DNS) resolves human-readable domain names to numerical IP addresses via recursive and authoritative name servers.
Network sockets provide endpoints for IPC over IP networks using IP address and port number.
"""
            }
        ]
    },
    {
        "filename": "CS104_Software_Engineering_Principles.pdf",
        "title": "CS104: Software Engineering & System Architecture",
        "pages": [
            {
                "heading": "Chapter 1: Software Development Lifecycle (SDLC)",
                "content": """
Software Engineering applies systematic principles to the design, development, testing, and maintenance of software systems.
Waterfall Model is a linear sequential SDLC model with distinct phases: Requirements, Design, Implementation, Testing, Deployment, Maintenance.
Agile Methodology emphasizes iterative development, flexible collaboration, customer involvement, and rapid response to change.
Scrum is an Agile framework structured around fixed-length Sprints (typically 2-4 weeks), daily standup meetings, Sprint Planning, Sprint Review, and Retrospectives.
User stories describe features from the perspective of an end-user and include acceptance criteria.
"""
            },
            {
                "heading": "Chapter 2: Software Architecture Styles",
                "content": """
Software architecture defines the high-level structure of software systems and component relationships.
Monolithic Architecture builds the entire application as a single unified deployable unit. Simple to start, but difficult to scale independently.
Microservices Architecture decomposes an application into independent, loosely coupled, independently deployable services communicating via HTTP/REST or gRPC.
Layered (N-Tier) Architecture organizes code into distinct logical layers: Presentation Layer, Business Logic Layer, Data Access Layer, and Database Layer.
Event-Driven Architecture decouples producers and consumers using asynchronous event streams via message brokers like Apache Kafka or RabbitMQ.
"""
            },
            {
                "heading": "Chapter 3: RESTful API Design & Principles",
                "content": """
Representational State Transfer (REST) is an architectural style for designing networked applications over HTTP.
REST Architectural Constraints: Client-Server separation, Statelessness, Cacheability, Uniform Interface, Layered System, and Code on Demand.
Standard HTTP Methods: GET (retrieve resource), POST (create resource), PUT (replace resource), PATCH (partial modification), DELETE (remove resource).
HTTP Status Codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error.
OpenAPI/Swagger provides standard specification for documenting RESTful API endpoints and schemas.
"""
            },
            {
                "heading": "Chapter 4: Quality Assurance & CI/CD Pipelines",
                "content": """
Software testing ensures software correctness, quality, and performance.
Testing Levels: Unit Testing (tests individual functions/classes), Integration Testing (tests component interactions), System Testing (tests entire integrated system), End-to-End Testing (simulates real user flows).
SOLID Principles for object-oriented design: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.
Continuous Integration (CI) automatically builds and runs test suites whenever code changes are committed.
Continuous Deployment (CD) automatically deploys validated code changes to production environments.
"""
            }
        ]
    }
]

def build_pdfs():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor='#1E293B',
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'ChapterHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor='#2563EB',
        spaceAfter=10
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=15,
        textColor='#334155',
        spaceAfter=12
    )

    for doc_info in documents:
        file_path = RAW_DATA_DIR / doc_info["filename"]
        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        story = []

        # Add Title
        story.append(Paragraph(doc_info["title"], title_style))
        story.append(Spacer(1, 10))

        for idx, p_info in enumerate(doc_info["pages"]):
            if idx > 0:
                story.append(PageBreak())
            story.append(Paragraph(p_info["heading"], heading_style))
            paragraphs = p_info["content"].strip().split("\n")
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), body_style))

        doc.build(story)
        print(f"Generated PDF: {file_path}")

if __name__ == "__main__":
    build_pdfs()
