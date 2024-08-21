REQUESTS_OBLIGATED = [
    {
        "websites":[
            ("name"),
            ("layers"),
            {
                "layers":[
                    ("cookies","static_status",{
                        "CONDITIONAL":[
                            ("cookies","static")
                        ]
                    }),
                    ("proxy","use_proxy",{
                        "CONDITIONAL":[
                            ("proxy","ip"),
                            ("proxy","type"),
                            ("proxy","port")
                        ]
                    }),
                    ("success_request"),
                    ("headers","type"),
                    ("data","type"),
                    ("data","actual_data"),
                ]
            }
        ]
    }
]


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}