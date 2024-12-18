package com.team3.scvs.repository;

import com.team3.scvs.entity.PSAEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

@Repository
public interface PSARepository extends JpaRepository<PSAEntity, Long> {
    // PSA 데이터베이스 작업을 처리하는 기본 메서드는 JpaRepository에서 제공됩니다.
    // 필요시 추가적인 쿼리 메서드를 정의할 수 있습니다.

    // 제목에 키워드가 포함된 공지사항 검색
    List<PSAEntity> findByTitleContaining(String keyword);

    // 작성일 기준 내림차순 정렬
    //List<PSA> findAllByOrderByPublishedAtDesc();

    // 공지 id 기준 내림차순 정렬
    List<PSAEntity> findAllByOrderByIdDesc();

    // 특정 기간 동안 작성된 공지사항 검색
    List<PSAEntity> findByPublishedAtBetween(LocalDateTime startDate, LocalDateTime endDate);

    // 가장 최근 작성된 공지사항 1개 반환
    PSAEntity findTopByOrderByPublishedAtDesc();

    // 페이지 단위로 공지사항 가져오기
    Page<PSAEntity> findAll(Pageable pageable);

    // 페이징 가능한 검색 메서드
    Page<PSAEntity> findByTitleContaining(String title, Pageable pageable);

    // id가 현재 id보다 큰 가장 작은 공지
    PSAEntity findFirstByIdGreaterThanOrderByIdAsc(Long id);

    // id가 현재 id보다 작은 가장 큰 공지
    PSAEntity findFirstByIdLessThanOrderByIdDesc(Long id);
}
