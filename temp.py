STYLE_TEMPLATE = """
                <style type="text/css">
                    table {
                            border-collapse: collapse;
                            }
                        table th,
                        table td {
                            padding: 0 10px;
                            }
                        table.brd th,
                        table.brd td {
                                border: 1px solid #000;
                                }
                        div {
                            background-color: white;
                            border-radius: 20px;
                            font-family: "Georgia", serif;
                            paddind-top: 10px;
                            padding-bottom: 10px;,
                            }
                        body {background-color: aliceblue;}
                </style>
                """

TABLE_TEMPLATE = """
                <body style="padding: 0 20%">
                <div style="padding: 0 16%">
                <h1 style="padding: 0 20%">Top of 85 users</h1>
                <table>
                <tr>
                    <th><h2>#</h2></th>
                    <th><h3>DisplayName</h3></th>
                    <th><h3>Age</h3></th>
                    <th><h3>Comments</h3></th>
                </tr>
                """

TABLE_END = """
            </table>
            </div>
            </body>
            """