package com.team3.scvs.service;

import com.team3.scvs.dto.PSADTO; // <변경됨> DTO import
import com.team3.scvs.entity.PSAEntity;
import com.team3.scvs.repository.PSARepository;
import com.team3.scvs.util.ConvertUtil; // <변경됨> ConvertUtil import
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors; // <변경됨> DTO 변환에 사용

@Service
public class PSAService {

    @Autowired
    private PSARepository psaRepository;

    // 모든 공지사항 조회 (공지 id순 정렬)
    public List<PSADTO> findAllPSAs() { // DTO 반환
        return psaRepository.findAllByOrderByIdDesc()
                .stream()
                .map(ConvertUtil::convertToDTO) // <변경됨> ConvertUtil 사용
                .collect(Collectors.toList()); // <변경됨> DTO 리스트로 변환
    }

    // 특정 공지사항 ID로 조회
    public PSADTO findPSAById(Long id) { // <변경됨> DTO 반환
        PSAEntity psaEntity = psaRepository.findById(id).orElse(null);
        return psaEntity != null ? ConvertUtil.convertToDTO(psaEntity) : null; // <변경됨> ConvertUtil 사용
    }

    // 제목으로 공지사항 검색
    public List<PSADTO> searchPSAsByTitle(String keyword) { // <변경됨> DTO 반환
        return psaRepository.findByTitleContaining(keyword)
                .stream()
                .map(ConvertUtil::convertToDTO) // <변경됨> ConvertUtil 사용
                .collect(Collectors.toList()); // <변경됨> DTO 리스트로 변환
    }

    // 특정 기간 동안 작성된 공지사항 조회
    public List<PSADTO> findPSAsWithinDateRange(LocalDateTime startDate, LocalDateTime endDate) { // <변경됨> DTO 반환
        return psaRepository.findByPublishedAtBetween(startDate, endDate)
                .stream()
                .map(ConvertUtil::convertToDTO) // <변경됨> ConvertUtil 사용
                .collect(Collectors.toList()); // <변경됨> DTO 리스트로 변환
    }

    // 새로운 공지사항 생성 또는 업데이트
    public void savePSA(PSADTO psaDTO) { // <변경됨> DTO를 매개변수로 받음
        PSAEntity psaEntity = ConvertUtil.convertToEntity(psaDTO); // <변경됨> ConvertUtil 사용
        psaRepository.save(psaEntity); // <변경됨> Entity 저장
    }

    public void updatePSA(Long id, String title, String content) {
        // ID로 PSAEntity 조회
        PSAEntity psaEntity = psaRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid PSA ID: " + id));

        // 데이터 업데이트
        psaEntity.setTitle(title);
        psaEntity.setContent(content);

        // 저장
        psaRepository.save(psaEntity);
    }

    // 특정 공지사항 삭제
    public void deletePSAById(Long id) {
        psaRepository.deleteById(id);
    }

    // 가장 최근 공지사항 조회
    public PSADTO findLatestPSA() { // <변경됨> DTO 반환
        PSAEntity psaEntity = psaRepository.findTopByOrderByPublishedAtDesc();
        return psaEntity != null ? ConvertUtil.convertToDTO(psaEntity) : null; // <변경됨> ConvertUtil 사용
    }

    // 페이지네이션 지원 공지사항 목록 조회
    public Page<PSADTO> findAllPSAsPaginated(int page, int size) { // <변경됨> DTO 반환
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "id"));
        return psaRepository.findAll(pageable)
                .map(ConvertUtil::convertToDTO); // <변경됨> ConvertUtil 사용
    }

    // 페이징을 지원하는 검색 기능
    public Page<PSADTO> searchPSAsByTitlePaginated(String query, int page, int size) { // <변경됨> DTO 반환
        Pageable pageable = PageRequest.of(page, size, Sort.by("publishedAt").descending());
        return psaRepository.findByTitleContaining(query, pageable)
                .map(ConvertUtil::convertToDTO); // <변경됨> ConvertUtil 사용
    }

    // 이전 공지
    public PSADTO findPreviousPSA(Long id) { // <변경됨> DTO 반환
        PSAEntity psaEntity = psaRepository.findFirstByIdGreaterThanOrderByIdAsc(id);
        return psaEntity != null ? ConvertUtil.convertToDTO(psaEntity) : null; // <변경됨> ConvertUtil 사용
    }

    // 다음 공지
    public PSADTO findNextPSA(Long id) { // <변경됨> DTO 반환
        PSAEntity psaEntity = psaRepository.findFirstByIdLessThanOrderByIdDesc(id);
        return psaEntity != null ? ConvertUtil.convertToDTO(psaEntity) : null; // <변경됨> ConvertUtil 사용
    }
}
