import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_meta_endpoint():
    res = client.get("/api/meta")
    assert res.status_code == 200
    data = res.json()
    assert "skills" in data
    assert "locations" in data
    assert "default_alpha" in data

def test_users_endpoints():
    # List users
    res = client.get("/api/users")
    assert res.status_code == 200
    users = res.json()
    assert len(users) > 0

    # Create new user
    new_user = {
        "name": "Test Student",
        "city": "Banani",
        "latitude": 23.7937,
        "longitude": 90.4066,
        "offers": [{"skill_name": "Web Development", "category": "Technology"}],
        "wants": [{"skill_name": "Graphic Design", "category": "Creative"}]
    }
    res_post = client.post("/api/users", json=new_user)
    assert res_post.status_code == 200
    created = res_post.json()
    assert created["name"] == "Test Student"

    # Delete user
    del_res = client.delete(f"/api/users/{created['id']}")
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"

    # Delete non-existent user
    del_fail = client.delete("/api/users/non-existent-user-id")
    assert del_fail.status_code == 404

def test_match_run_and_cycles():
    payload = {
        "alpha": 0.6,
        "min_k": 3,
        "max_k": 4
    }
    res = client.post("/api/match/run", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "cycles" in data
    assert "graph" in data
    assert data["graph"]["total_nodes"] > 0

    # Test cached cycles
    res_cached = client.get("/api/match/cycles")
    assert res_cached.status_code == 200
    assert len(res_cached.json()) == data["cycles_count"]

def test_proposals_workflow_api():
    # Run match to ensure cycles in cache
    res = client.post("/api/match/run", json={"alpha": 0.5, "min_k": 3, "max_k": 4})
    data = res.json()
    cycles = data["cycles"]
    assert len(cycles) > 0

    target_cycle = cycles[0]
    cycle_id = target_cycle["id"]

    # Create proposal
    res_p = client.post("/api/proposals/create", json={"cycle_id": cycle_id, "expiration_seconds": 3600})
    assert res_p.status_code == 200
    prop = res_p.json()
    prop_id = prop["id"]
    assert prop["status"] == "PENDING"

    # Test create with invalid cycle
    bad_p = client.post("/api/proposals/create", json={"cycle_id": "non-existent-cycle-999"})
    assert bad_p.status_code == 404

    # List proposals
    res_list = client.get("/api/proposals")
    assert res_list.status_code == 200
    assert any(p["id"] == prop_id for p in res_list.json())

    # Respond to proposal with invalid user
    bad_resp = client.post(f"/api/proposals/{prop_id}/respond", json={"user_id": "invalid-user", "response": "ACCEPTED"})
    assert bad_resp.status_code == 400

    # Respond properly with first user
    first_user = target_cycle["user_ids"][0]
    res_resp = client.post(f"/api/proposals/{prop_id}/respond", json={"user_id": first_user, "response": "ACCEPTED"})
    assert res_resp.status_code == 200

def test_synthetic_and_benchmarks():
    # Generate synthetic population
    res_synth = client.post("/api/synthetic/generate", json={"count": 25})
    assert res_synth.status_code == 200
    assert res_synth.json()["generated_users"] == 25

    # Run benchmarks
    res_bench = client.post("/api/synthetic/benchmark", json={"node_counts": [10, 20]})
    assert res_bench.status_code == 200
    data = res_bench.json()
    assert "benchmark_results" in data
    assert len(data["benchmark_results"]) == 2

def test_reset_and_root():
    res_reset = client.post("/api/reset")
    assert res_reset.status_code == 200
    assert res_reset.json()["status"] == "success"

    res_root = client.get("/")
    assert res_root.status_code == 200
