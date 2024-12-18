package com.team3.scvs.repository;

import com.team3.scvs.entity.KorEntity;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface KorRepository extends JpaRepository<KorEntity, Long> {
    @Query("SELECT k FROM KorEntity k ORDER BY k.korEconNewsId DESC, k.publishedAt DESC")
    List<KorEntity> findTop5ByOrderByKorEconNewsIdDescPublishedAtDesc(Pageable pageable);
}
