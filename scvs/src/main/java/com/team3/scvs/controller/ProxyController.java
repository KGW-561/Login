package com.team3.scvs.controller;

import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/proxy")
public class ProxyController {

    @GetMapping("/fetch")
    public ResponseEntity<?> proxyFetch(@RequestParam String url) {
        try {
            // RestTemplate로 외부 API 호출
            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.set("User-Agent", "Mozilla/5.0"); // Yahoo API가 User-Agent를 요구

            HttpEntity<String> entity = new HttpEntity<>(headers);

            // Yahoo API 요청
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);

            // 응답 반환 (CORS 헤더 포함)
            return ResponseEntity.ok()
                    .header("Access-Control-Allow-Origin", "*")
                    .header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                    .body(response.getBody());
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Proxy request failed: " + e.getMessage());
        }
    }
}
