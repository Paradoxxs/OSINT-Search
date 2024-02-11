import dns.resolver


class dnsresolver():
    record_type = ["MX","ns","TXT"]

    async def query(self,domain):
        data = []
        for record in self.record_type:
            answers = dns.resolver.resolve(domain,record)
            for rdata in answers:
                data.append(rdata)
        return data
    async def domain2IP(self,domain):
        answer = dns.resolver.resolve(domain)
        return answer

        